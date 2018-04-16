import feedparser
import bs4

from sources import Source


AFTERIOC = 'Indicators of Compromise'


class RSS(Source):

    def __init__(self, name, url, feed_type):
        self.name = name
        self.url = url
        self.feed_type = feed_type

    def run(self, saved_state):

        feed = feedparser.parse(self.url)

        artifacts = []
        for item in list(reversed(feed['items'])):
            # only new items
            published_parsed = item.get('published_parsed') or item.get('updated_parsed')
            if published_parsed <= feedparser._parse_date(saved_state):
                continue

            try:
                soup = bs4.BeautifulSoup(item['content'][0]['value'], 'html.parser')
            except KeyError:
                soup = bs4.BeautifulSoup(item['summary'], 'html.parser')

            # do some preprocessing to remove common obfuscation methods
            [x.unwrap() for x in soup.find_all('strong')]
            [x.unwrap() for x in soup.find_all('b')]
            [x.unwrap() for x in soup.find_all('em')]
            [x.unwrap() for x in soup.find_all('i')]
            soup = bs4.BeautifulSoup(unicode(soup), 'html.parser')

            text = ''
            if self.feed_type == 'afterioc':
                text = soup.get_text(separator=' ').split(AFTERIOC)[-1]
                artifacts += self.process_element(text, item.get('link') or self.url, include_nonobfuscated=True)
            elif self.feed_type == 'clean':
                text = soup.get_text(separator=' ')
                artifacts += self.process_element(text, item.get('link') or self.url, include_nonobfuscated=True)
            else:
                # default: self.feed_type == 'messy'
                text = soup.get_text(separator=' ')
                artifacts += self.process_element(text, item.get('link') or self.url)

            saved_state = item.get('published') or item.get('updated')

        return saved_state, artifacts
