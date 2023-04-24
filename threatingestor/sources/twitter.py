from __future__ import absolute_import

import os
import random
import string
import twitter
import requests
from loguru import logger
from pyshorteners import Shortener, exceptions

try:
    import numpy as np
    installed_np = True
except ImportError:
    logger.warning("Missing the following package(s): numpy")
    installed_np = False

try:
    import cv2
    installed_cv = True
except ImportError:
    logger.warning("Missing the following package(s): opencv-python")
    installed_cv = False

try:
    import pytesseract
    installed_tesseract = True
except ImportError:
    logger.warning("Missing the following package(s): pytesseract")
    installed_tesseract = False

from threatingestor.sources import Source

TWEET_URL = 'https://twitter.com/{user}/status/{id}'

s = Shortener()

# Creates a random string with a length of 5
def tmp_name():
    return "".join(random.choice(string.ascii_lowercase) for _ in range(5))

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

        tweets = []
        
        for tweet in tweet_list:
            if "retweeted_status" in tweet:
                content = tweet['retweeted_status'].get('full_text', '')
            else:
                content = tweet.get('full_text', '')

            tweets.append({
                'content': content,
                'id': tweet.get('id_str', ''),
                'user': tweet.get('user', {}).get('screen_name', ''),
                'entities': tweet.get('entities', {}),
            })

        artifacts = []

        # Traverse in reverse, old to new.
        tweets.reverse()

        tmp_file = str(tmp_name())

        for tweet in tweets:

            # Expand t.co links.
            for url in tweet['entities'].get('urls', []):
                try:
                    tweet['content'] = tweet['content'].replace(url['url'], url['expanded_url'])
                except KeyError:
                    
                    # Attempts to expand the URL if not available through Twitter
                    try:
                        tweet['content'] = tweet['content'].replace(url['url'], str(s.tinyurl.expand(url['url'])))
                    except exceptions.ExpandingErrorException:
                        # If unable to expand the URL, this exception is thrown
                        pass

            # Process tweet
            saved_state = tweet['id']
            artifacts += self.process_element(tweet['content'], TWEET_URL.format(user=tweet['user'], id=tweet['id']), include_nonobfuscated=self.include_nonobfuscated)

            if installed_cv and installed_np:

                for media_url in tweet['entities'].get('media', []):
                    img = media_url["media_url_https"]

                    if "http" in img:
                        with open(f"/tmp/{tmp_file}", "wb") as i:
                            i.write(requests.get(str(img)).content)

                    if os.path.exists(f"/tmp/{tmp_file}"):
                        data = cv2.imread(f"/tmp/{tmp_file}")
                    else:
                        # No image is present
                        try:
                            data = cv2.imread(img)
                        except TypeError:
                            pass
                        
                    try:
                        # Creates a binary image by using the proper threshold from cv + converts to grayscale
                        # Inverts the binary
                        invert_img = cv2.bitwise_not(cv2.threshold(cv2.cvtColor(data, cv2.COLOR_BGR2GRAY), 130, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1])

                        # Helps with cleanup
                        process_iter = cv2.dilate(cv2.erode(invert_img, np.ones((2,2), np.uint8), iterations=1), np.ones((2,2), np.uint8), iterations=1)

                        if installed_tesseract:
                            # Converts image data to a string
                            img_data = pytesseract.image_to_string(process_iter)
                        else:
                            img_data = ""

                        # Process media
                        saved_state = tweet['id']
                        artifacts += self.process_element(img_data, img, include_nonobfuscated=self.include_nonobfuscated)

                        os.remove(f"/tmp/{tmp_file}")
                            
                    except cv2.error:
                        raise FileNotFoundError

        return saved_state, artifacts
