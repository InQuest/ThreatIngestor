from __future__ import absolute_import


import re
import requests
import twitter
from loguru import logger
from threatingestor.sources import Source


TWEET_URL = 'https://twitter.com/{user}/status/{id}'

WHITELIST_DOMAINS = r"pastebin\.com"


class Plugin(Source):

    def __init__(self, name, api_key, api_secret_key, access_token, access_token_secret, defanged_only=True, **kwargs):
        self.name = name
        self.api = twitter.Twitter(auth=twitter.OAuth(access_token, access_token_secret, api_key, api_secret_key))

        # Let the user decide whether to include non-obfuscated URLs or not.
        self.include_nonobfuscated = not defanged_only

        # Support for full tweet
        tweet_param = {'tweet_mode': 'extended'}
        kwargs.update(tweet_param)

        # Forward kwargs.
        # NOTE: No validation is done here, so if the config is wrong, expect bad results.
        self.kwargs = kwargs

        # Decide which endpoint to use based on passed arguments.
        # If slug and owner_screen_name, use List API.
        # If screen_name or user_id, use User Timeline API.
        # If q is set, use Search API.
        # Otherwise, default to mentions API.
        self.endpoint = self.api.statuses.mentions_timeline
        if (kwargs.get('slug') and kwargs.get('owner_screen_name')) or (kwargs.get('list_id') and kwargs.get('owner_screen_name')):
            self.endpoint = self.api.lists.statuses
        elif kwargs.get('screen_name') or kwargs.get('user_id'):
            self.endpoint = self.api.statuses.user_timeline
        elif kwargs.get('q'):
            self.endpoint = self.api.search.tweets

    def run(self, saved_state):
        # Modify kwargs to insert since_id.
        if saved_state:
            self.kwargs['since_id'] = saved_state

        # Pull new tweets.
        try:
            response = self.endpoint(**self.kwargs)
        except twitter.api.TwitterHTTPError as e:
            # API error; log and return early.
            logger.warning(f"Twitter API Error: {e}")

            return saved_state, []

        # Correctly handle responses from different endpoints.
        try:
            tweet_list = response['statuses']
        except TypeError:
            tweet_list = response

        tweets = [{
            'content': s.get('full_text', ''),
            'id': s.get('id_str', ''),
            'user': s.get('user', {}).get('screen_name', ''),
            'entities': s.get('entities', {}),
        } for s in tweet_list]

        artifacts = []
        # Traverse in reverse, old to new.
        tweets.reverse()
        for tweet in tweets:

            # Expand t.co links.
            for url in tweet['entities'].get('urls', []):
                try:
                    tweet['content'] = tweet['content'].replace(url['url'], url['expanded_url'])

                    # Check if pastebin.com in url
                    if re.search(WHITELIST_DOMAINS, url['expanded_url']):

                        # Check if the url is already returning the 'raw' pastebin. If not, update the url
                        if 'raw' not in url['expanded_url']:
                            pastebin_id = re.search(r"pastebin.com/(.*?)$", url['expanded_url']).group(1)
                            location = f"https://pastebin.com/raw/{pastebin_id}"
                        else:
                            location = url['expanded_url']

                        req = requests.get(location)
                        saved_state = tweet['id']
                        artifacts += self.process_element(req.text, location, include_nonobfuscated=True)

                        logger.log('NOTIFY', f"Discovered paste: {location}")

                except KeyError:
                    # No url/expanded_url, continue without expanding.
                    pass

        return saved_state, artifacts




