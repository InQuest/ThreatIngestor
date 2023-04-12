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
        saved_state = datetime.datetime.utcnow().isoformat()[:-7] + "Z"

        # Configures sitemap parsing
        response = requests.get(self.url)
        xml = BeautifulSoup(response.text, "lxml-xml")

        sitemapindex = xml.find_all("sitemapindex")
        sitemap = xml.find_all("urlset")

        if sitemapindex:
            get_sitemap_type = "sitemapindex"
        elif sitemap:
            get_sitemap_type = "urlset"
        
        sitemaps = xml.find_all("sitemap")

        try:
            get_child_sitemaps = []

            for sitemap in sitemaps:
                get_child_sitemaps.append(sitemap.findNext("loc").text)

            if get_sitemap_type == "sitemapindex":
                sitemaps = get_child_sitemaps
        
        except UnboundLocalError:
            sitemaps = [self.url]

        urls = xml.find_all("url")
        artifacts = []

        for sitemap in sitemaps:
            for url in urls:

                # Extracts only the 'loc' tag from the xml
                if xml.find("loc"):
                    loc = url.findNext("loc").text
                    parsed_uri = urlparse(loc)
                    domain = "{uri.netloc}".format(uri=parsed_uri)
                else:
                    loc = ""
                    domain = ""

                row = {
                    "domain": domain,
                    "loc": loc
                }

                if self.filter is not None:
                    # Regex input via config.yml
                    xml_query = re.compile(r"{0}".format(self.filter)).findall(str(self.filter.split('|')))

                    # Iterates over the regex output to locate all provided keywords
                    for x in xml_query:
                        # Uses a path instead of a keyword
                        if self.path is not None:
                            provided_path = f"{self.path}{x}"

                            if provided_path in row["loc"]:
                                artifacts += self.process_element(row["loc"], self.url)
                        
                        # Only filters using a keyword
                        if self.path is None:
                            if x in row["loc"]:
                                artifacts += self.process_element(row["loc"], self.url)
                
                elif self.filter is None and self.path is not None:
                    # Filters only by path in XML loc, no set filter
                    # Default: /path/name/*
                    provided_path = f"{self.path}"

                    if provided_path in row["loc"]:
                        artifacts += self.process_element(row["loc"], self.url)
                
                else:
                    # Locates all blog links within the sitemap
                    if "blog" in row["loc"]:
                        artifacts += self.process_element(row["loc"], self.url)
        
        return saved_state, artifacts