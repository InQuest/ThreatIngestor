import datetime
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from threatingestor.sources import Source

class Plugin(Source):
    
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def run(self, saved_state):
        saved_state = datetime.datetime.utcnow().isoformat()[:-7] + "Z"

        # Configures sitemap parsing
        response = urllib.request.urlopen(self.url)
        xml = BeautifulSoup(response, "lxml-xml", from_encoding=response.info().get_param("charset"))

        sitemapindex = xml.find_all("sitemapindex")
        sitemap = xml.find_all("urlset")

        if sitemapindex:
            get_sitemap_type = "sitemapindex"
        elif sitemap:
            get_sitemap_type = "urlset"
        
        sitemaps = xml.find_all("sitemap")

        get_child_sitemaps = []

        for sitemap in sitemaps:
            get_child_sitemaps.append(sitemap.findNext("loc").text)

        if get_sitemap_type == "sitemapindex":
            sitemaps = get_child_sitemaps
        else:
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

                # Locates all blog links within the sitemap
                if "blog" in row["loc"]:
                    print(row["loc"])
                    artifacts += self.process_element(row["loc"], self.url)
        
        return saved_state, artifacts