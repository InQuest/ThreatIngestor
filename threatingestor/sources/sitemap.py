import requests
import datetime
import regex as re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from threatingestor.sources import Source

class Plugin(Source):

    def __init__(self, name, url, filter=None, path=None):
        self.name = name
        self.url = url
        self.filter = filter
        self.path = path

    def run(self, saved_state):
        # Configures sitemap parsing
        response = requests.get(self.url)
        xml = BeautifulSoup(response.text, "lxml-xml")

        urls = xml.find_all("url")
        text = ""
        artifacts = []

        for u in urls:
            if saved_state and xml.find("lastmod") and saved_state <= str(u.findNext("lastmod").text).split("T", 1)[0]:
                continue

            # Extracts only the 'loc' tag from the xml
            if xml.find("loc"):
                loc = u.findNext("loc").text
                response = requests.get(loc)
                soup = BeautifulSoup(response.text, 'html.parser')
            else:
                continue

            if response.status_code >= 400:
                continue

            [x.unwrap() for x in soup.find_all('strong')]
            [x.unwrap() for x in soup.find_all('b')]
            [x.unwrap() for x in soup.find_all('em')]
            [x.unwrap() for x in soup.find_all('i')]
            soup = BeautifulSoup(soup.decode(), 'html.parser')

            if self.filter is not None:
                # Regex input via config.yml
                # Example: security|threat|malware
                xml_query = re.compile(r"{0}".format(self.filter)).findall(str(self.filter.split('|')))

                # Iterates over the regex output to locate all provided keywords
                for x in xml_query:
                    # Uses a path instead of a keyword
                    if self.path is not None:
                        if self.path in loc:
                            text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                            artifacts += self.process_element(content=text, reference_link=self.url, include_nonobfuscated=True)

                    # Only filters using a keyword
                    if self.path is None:
                        if x in loc:
                            text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                            artifacts += self.process_element(content=text, reference_link=self.url, include_nonobfuscated=True)

            elif self.filter is None and self.path is not None:
                # Filters only by path in XML loc, no set filter
                # Default: /path/name/*

                if self.path in loc:
                    text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                    artifacts += self.process_element(content=text, reference_link=self.url, include_nonobfuscated=True)
            
            else:
                # Locates all blog links within the sitemap
                if "blog" in loc:
                    text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                    artifacts += self.process_element(content=text, reference_link=self.url, include_nonobfuscated=True)

            if xml.find("lastmod"):
                saved_state = str(u.findNext("lastmod").text).split("T", 1)[0]
            else:
                saved_state = str(datetime.date.today())

        return saved_state, artifacts
