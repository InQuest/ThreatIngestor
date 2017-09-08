from __future__ import absolute_import

import twitter

from sources import Source


TWEET_URL = 'https://twitter.com/statuses/{id}'


class Twitter(Source):

    def __init__(self, owner_screen_name, slug, token, token_key, con_secret_key, con_secret):
        self.owner_screen_name = owner_screen_name
        self.slug = slug
        self.api = twitter.Twitter(auth=twitter.OAuth(token, token_key, con_secret, con_secret_key))

    def run(self, saved_state):

        # preform kwargs because twitter lib doesnt do any checking
        kwargs = {
            'owner_screen_name': self.owner_screen_name,
            'slug': self.slug,
        }
        if saved_state:
            kwargs['since_id'] = saved_state

        # pull new tweets
        tweets = [{
            'content': s['text'],
            'id': s['id_str']
        } for s in self.api.lists.statuses(**kwargs)]
        
        artifacts = []
        # traverse in reverse, old to new
        tweets.reverse()
        for tweet in tweets:
            saved_state = tweet['id']
            artifacts += self.process_element(tweet['content'], TWEET_URL.format(id=tweet['id']))

        return saved_state, artifacts
