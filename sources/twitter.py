from __future__ import absolute_import

import twitter

from sources import Source


TWEET_URL = 'https://twitter.com/statuses/{id}'


class Twitter(Source):

    def __init__(self, token, token_key, con_secret_key, con_secret, **kwargs):
        self.api = twitter.Twitter(auth=twitter.OAuth(token, token_key, con_secret, con_secret_key))

        # forward kwargs.
        # NOTE: no validation is done here, so if the config is wrong, expect bad results.
        self.kwargs = kwargs

        # decide which endpoint to use based on passed arguments.
        # if slug and owner_screen_name, use List API.
        # if screen_name or user_id, use User Timeline API.
        # otherwise, default to Search API.
        self.endpoint = self.api.search.tweets
        if kwargs.get('slug') and kwargs.get('owner_screen_name'):
            self.endpoint = self.api.lists.statuses
        elif kwargs.get('screen_name') or kwargs.get('user_id'):
            self.endpoint = self.api.statuses.user_timeline

    def run(self, saved_state):

        # modify kwargs to insert since_id
        if saved_state:
            self.kwargs['since_id'] = saved_state

        # pull new tweets
        response = self.endpoint(**self.kwargs)
        # correctly handle responses from different endpoints
        try:
            tweet_list = response['statuses']
        except TypeError:
            tweet_list = response
        tweets = [{
            'content': s['text'],
            'id': s['id_str']
        } for s in tweet_list]

        artifacts = []
        # traverse in reverse, old to new
        tweets.reverse()
        for tweet in tweets:
            saved_state = tweet['id']
            artifacts += self.process_element(tweet['content'], TWEET_URL.format(id=tweet['id']))

        return saved_state, artifacts
