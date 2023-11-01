import requests
import datetime
import regex as re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from threatingestor.sources import Source

class Plugin(Source):

    def __init__(self, name, url, include=None, exclude=None, path=None):
        self.name = name
        self.url = url
        self.include = include
        self.exclude = exclude
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
                try:
                    response = requests.get(loc)
                    soup = BeautifulSoup(response.text, 'html.parser')
                except requests.exceptions.ConnectTimeout:
                    continue
            else:
                continue

            if response.status_code >= 400:
                continue

            [x.unwrap() for x in soup.find_all('strong')]
            [x.unwrap() for x in soup.find_all('b')]
            [x.unwrap() for x in soup.find_all('em')]
            [x.unwrap() for x in soup.find_all('i')]
            soup = BeautifulSoup(soup.decode(), 'html.parser')

            if self.exclude is not None:
                # Regex input via config.yml
                xml_exclude = re.sub(re.compile(fr"{self.exclude}", re.IGNORECASE), "", str(loc))

                if xml_exclude:
                    if self.path is None and "http" in xml_exclude:
                        text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                        artifacts += self.process_element(content=text, reference_link=str(loc), include_nonobfuscated=True)

                    # Uses a path instead of a keyword
                    if self.path is not None:
                        if self.path in xml_exclude:
                            text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                            artifacts += self.process_element(content=text, reference_link=str(loc), include_nonobfuscated=True)

            if self.include is not None:
                # Regex input via config.yml
                # Example: security|threat|malware
                xml_include = re.compile(r"{0}".format(self.include)).findall(str(self.include.split('|')))

                # Iterates over the regex output to locate all provided keywords
                for xi in xml_include:
                    # Uses a path instead of a keyword
                    if self.path is not None:
                        if self.path in loc:
                            text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                            artifacts += self.process_element(content=text, reference_link=str(loc), include_nonobfuscated=True)

                    # Only filters using a keyword
                    if self.path is None:
                        if xi in loc:
                            text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                            artifacts += self.process_element(content=text, reference_link=str(loc), include_nonobfuscated=True)

            if self.include is None and self.exclude is None and self.path is not None:
                # Filters only by path in XML loc, no set include
                # Default: /path/name/*

                if self.path in loc:
                    text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                    artifacts += self.process_element(content=text, reference_link=str(loc), include_nonobfuscated=True)
            
            if self.include is None and self.exclude is None and self.path is None:
                # Locates all blog links within the sitemap
                if "blog" in loc:
                    text = soup.get_text(separator=' ').split('Indicators of Compromise')[-1]
                    artifacts += self.process_element(content=text, reference_link=str(loc), include_nonobfuscated=True)

            if xml.find("lastmod"):
                saved_state = str(u.findNext("lastmod").text).split("T", 1)[0]
            else:
                saved_state = str(datetime.date.today())

        return saved_state, artifacts
