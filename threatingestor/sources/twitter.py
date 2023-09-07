from __future__ import absolute_import

import twitter, requests
from loguru import logger

from threatingestor.sources import Source

class Plugin(Source):

    def __init__(self, name, api_key, api_secret_key, access_token, access_token_secret, bearer_token, defanged_only=True, **kwargs):
        self.name = name
        self.bearer_token = bearer_token

        """
        Depending on the endpoint being used, we need to modify the type of authentiation being used
        How to identity the type of authentication = https://developer.twitter.com/en/docs/authentication/overview
        """
        self.auth = {
            "OAuth": twitter.Twitter(auth=twitter.OAuth(token=access_token,
                                                        token_secret=access_token_secret,
                                                        consumer_key=api_key,
                                                        consumer_secret=api_secret_key),
                                                        api_version="1.1"),
            "OAuth2": twitter.Twitter(auth=twitter.OAuth2(bearer_token=self.bearer_token), api_version="2", format="")
        }

        # Let the user decide whether to include non-obfuscated URLs or not.
        self.include_nonobfuscated = not defanged_only

        # Forward kwargs.
        # NOTE: No validation is done here, so if the config is wrong, expect bad results.
        self.kwargs = kwargs
        self.endpoint = None

    def run(self, saved_state):
        # Modify kwargs to insert since_id.
        if saved_state:
            self.kwargs['since_id'] = saved_state

        artifacts = []

        def bearer_oauth2(r):
            r.headers['Authorization'] = f"Bearer {self.bearer_token}"
            r.headers['User-Agent'] = "InQuestThreatIngestor"
            return r

        if self.kwargs.get('list_id'):
            list_url = f"https://api.twitter.com/2/lists/{self.kwargs.get('list_id')}/tweets"
            self.endpoint = requests.get(url=list_url, auth=bearer_oauth2, params="tweet.fields=lang,author_id")

            for tweet in self.endpoint.json()['data']:
                artifacts += self.process_element(content=tweet['text'], reference_link=f"https://twitter.com/InQuest/status/{tweet['id']}", include_nonobfuscated=self.include_nonobfuscated)

        if self.kwargs.get('username') or self.kwargs.get('user_id'):
            try:
                # Get the id of the username
                user_id = self.kwargs.get('user_id') or self.auth['OAuth2'].users.by.username._username(_username=self.kwargs.get('username'))["data"]["id"]
                self.endpoint = self.auth['OAuth2'].users._id.tweets(_id=user_id)
            except twitter.api.TwitterHTTPError as e:
                # API error; log and return early
                logger.warning(f"Twitter API Error: {e}")
                return saved_state, []

            for tweet in self.endpoint['data']:
                saved_state = tweet['id']
                artifacts += self.process_element(content=tweet['text'], reference_link=f"https://twitter.com/InQuest/status/{tweet['id']}", include_nonobfuscated=self.include_nonobfuscated)
        
        if self.kwargs.get('query'):
            try:
                self.endpoint = self.auth['OAuth2'].tweets.search.recent(query=self.kwargs.get('query'))
            except twitter.api.TwitterHTTPError as e:
                # API error; log and return early
                logger.warning(f"Twitter API Error: {e}")
                return saved_state, []

            for tweet in self.endpoint['data']:
                saved_state = tweet['id']
                artifacts += self.process_element(content=tweet['text'], reference_link=f"https://twitter.com/InQuest/status/{tweet['id']}", include_nonobfuscated=self.include_nonobfuscated)

        # No endpoint specified, return early
        if not self.endpoint:
            return saved_state, []

        return saved_state, artifacts
