from __future__ import absolute_import
import re


import twitter
from loguru import logger


from threatingestor.operators import Operator
import threatingestor.artifacts
import threatingestor.exceptions


TWEET_URL = re.compile(r'https://twitter\.com/\w{1,15}/status/\d+')


class Plugin(Operator):
    """Operator for Twitter."""
    def __init__(self, api_key, api_secret_key, access_token, access_token_secret, status, **kwargs):
        self.api = twitter.Twitter(auth=twitter.OAuth(access_token, access_token_secret, api_key, api_secret_key))
        self.status = status

        # Validate status, for better error handling.
        if not isinstance(self.status, str):
            raise threatingestor.exceptions.IngestorError(f"Invalid 'status' config: {self.status}")

        super(Plugin, self).__init__(kwargs.get('artifact_types'),
                                     kwargs.get('filter_string'),
                                     kwargs.get('allowed_sources'))
        self.artifact_types = kwargs.get('artifact_types') or [
            threatingestor.artifacts.URL,
            threatingestor.artifacts.Domain,
            threatingestor.artifacts.Hash,
            threatingestor.artifacts.IPAddress,
        ]


    def handle_artifact(self, artifact):
        """Operate on a single artifact."""
        status = artifact.format_message(self.status)

        # If artifact.reference_link is a tweet permalink, quote-tweet it.
        quote_tweet = None
        if TWEET_URL.match(artifact.reference_link):
            quote_tweet = artifact.reference_link

        self._tweet(status, quote_tweet=quote_tweet)


    def _tweet(self, status, quote_tweet=None):
        """Send content to Twitter as a status update."""
        try:
            return self.api.statuses.update(status=status,
                                            attachment_url=quote_tweet,
                                            tweet_mode='extended')
        except twitter.api.TwitterHTTPError as e:
            logger.warning(f"Twitter API Error: {e}")
            return None
