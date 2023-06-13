import requests
import datetime
import regex as re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from threatingestor.sources import Source
import threatingestor.artifacts

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
        artifacts_list = []

        for u in urls:

            # Extracts only the 'loc' tag from the xml
            if xml.find("loc"):
                loc = u.findNext("loc").text
            else:
                loc = ""

            if self.filter is not None:
                # Regex input via config.yml
                # Example: security|threat|malware
                xml_query = re.compile(r"{0}".format(self.filter)).findall(str(self.filter.split('|')))

                # Iterates over the regex output to locate all provided keywords
                for x in xml_query:
                    # Uses a path instead of a keyword
                    if self.path is not None:
                        if self.path in loc:
                            artifacts_list.append(loc)
                    
                    # Only filters using a keyword
                    if self.path is None:
                        if x in loc:
                            artifacts_list.append(loc)
            
            elif self.filter is None and self.path is not None:
                # Filters only by path in XML loc, no set filter
                # Default: /path/name/*

                if self.path in loc:
                    artifacts_list.append(loc)
            
            else:
                # Locates all blog links within the sitemap
                if "blog" in loc:
                    artifacts_list.append(loc)

        artifacts = []

        for a in artifacts_list:
            description = 'URL: {u}\nTask autogenerated by ThreatIngestor from source: {s}'.format(u=a, s=self.name)
            artifact = threatingestor.artifacts.URL(a, self.name, reference_link=self.url, reference_text=description)
            artifacts.append(artifact)

        # print(artifacts)
        saved_state = datetime.datetime.utcnow().isoformat()[:-7] + "Z"

        return saved_state, artifacts
