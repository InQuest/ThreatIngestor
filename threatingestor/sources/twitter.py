from __future__ import absolute_import

import twitter
from loguru import logger

from threatingestor.sources import Source

class Plugin(Source):

    def __init__(self, name, api_key, api_secret_key, access_token, access_token_secret, bearer_token=None, defanged_only=True, **kwargs):
        self.name = name

        """
        Depending on the endpoint being used, we need to modify the type of authentiation being used
        How to identity the type of authentication = https://developer.twitter.com/en/docs/authentication/overview
        """
        self.auth = {
            "OAuth": twitter.Twitter(auth=twitter.OAuth(access_token, access_token_secret, api_key, api_secret_key), api_version="1.1"),
            "OAuth2": twitter.Twitter(auth=twitter.OAuth2(bearer_token=bearer_token), api_version="2", format="")
        }

        # Let the user decide whether to include non-obfuscated URLs or not.
        self.include_nonobfuscated = not defanged_only

        # Forward kwargs.
        # NOTE: No validation is done here, so if the config is wrong, expect bad results.
        self.kwargs = kwargs

        # Decide which endpoint to use based on passed arguments.
        # If slug and owner_screen_name, use List API.
        # If screen_name or user_id, use User Timeline API.
        # If query is set, use Search API.
        # Otherwise, default to mentions API.
        self.endpoint = self.auth['OAuth2'].statuses.mentions_timeline
        if kwargs.get('id'):
            self.endpoint = self.auth['OAuth'].lists.statuses
        elif kwargs.get('screen_name') or kwargs.get('user_id'):
            self.endpoint = self.auth['OAuth'].statuses.user_timeline
        elif kwargs.get('query'):
            self.endpoint = self.auth['OAuth2'].tweets.search.recent

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

        artifacts = []
        
        for tweet in response['data']:
            saved_state = tweet['id']
            artifacts += self.process_element(tweet['text'], tweet['id'], include_nonobfuscated=self.include_nonobfuscated)

        return saved_state, artifacts
