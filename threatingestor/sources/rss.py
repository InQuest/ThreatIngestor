import bs4
import feedparser
import regex as re

try:
    # feedparser 5.x
    from feedparser import _parse_date
except ImportError:
    # feedparser 6.x
    from feedparser.datetimes import _parse_date

from threatingestor.sources import Source

class Plugin(Source):

    def __init__(self, name, url, feed_type, include=None, exclude=None):
        self.name = name
        self.url = url
        self.feed_type = feed_type
        self.include = include
        self.exclude = exclude

    def run(self, saved_state):
        feed = feedparser.parse(self.url)

        artifacts = []

        for item in list(reversed(feed['items'])):
            # Only new items
            published_parsed = item.get('published_parsed') or item.get('updated_parsed')

            if published_parsed and published_parsed <= _parse_date(saved_state or '0001-01-01'):
                continue

            try:
                soup = bs4.BeautifulSoup(item['content'][0]['value'], 'html.parser')
            except KeyError:
                try:
                    soup = bs4.BeautifulSoup(item['summary'], 'html.parser')
                except KeyError:
                    # Can't find any feed content, just skip this entry
                    continue

            # do some preprocessing to remove common obfuscation methods
            [x.unwrap() for x in soup.find_all('strong')]
            [x.unwrap() for x in soup.find_all('b')]
            [x.unwrap() for x in soup.find_all('em')]
            [x.unwrap() for x in soup.find_all('i')]
            soup = bs4.BeautifulSoup(soup.decode(), 'html.parser')

            text = ""

            if self.exclude is not None:
                rss_exclude = re.sub(re.compile(fr"{self.exclude}", re.IGNORECASE), "", str(item.get('link')))

                if rss_exclude:
                    if "http" in rss_exclude:
                        if self.feed_type == "afterioc":
                            text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                            artifacts += self.process_element(text, item.get('link'), include_nonobfuscated=True)
                        elif self.feed_type == "clean":
                            text = soup.get_text(separator=' ')
                            artifacts += self.process_element(text, item.get('link'), include_nonobfuscated=True)
                        else:
                            # Default: self.feed_type == 'messy'.
                            text = soup.get_text(separator=' ')
                            artifacts += self.process_element(text, item.get('link'))

            if self.include is not None:
                rss_include = re.compile(r"{0}".format(self.include)).findall(str(self.include.split('|')))

                for rss_f in rss_include:
                    if rss_f in item.get('link'):
                        if self.feed_type == "afterioc":
                            text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                            artifacts += self.process_element(text, item.get('link') or self.url, include_nonobfuscated=True)
                        elif self.feed_type == "clean":
                            text = soup.get_text(separator=' ')
                            artifacts += self.process_element(text, item.get('link') or self.url, include_nonobfuscated=True)
                        else:
                            # Default: self.feed_type == 'messy'.
                            text = soup.get_text(separator=' ')
                            artifacts += self.process_element(text, item.get('link') or self.url)

            if self.include is None and self.exclude is None:
                if self.feed_type == "afterioc":
                    text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                    artifacts += self.process_element(text, item.get('link') or self.url, include_nonobfuscated=True)
                elif self.feed_type == "clean":
                    text = soup.get_text(separator=' ')
                    artifacts += self.process_element(text, item.get('link') or self.url, include_nonobfuscated=True)
                else:
                    # Default: self.feed_type == 'messy'.
                    text = soup.get_text(separator=' ')
                    artifacts += self.process_element(text, item.get('link') or self.url)

            saved_state = item.get('published') or item.get('updated')

        return saved_state, artifacts
