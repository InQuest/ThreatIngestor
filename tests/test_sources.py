import unittest

import httpretty

import sources.rss
import sources.twitter


class TestRSS(unittest.TestCase):

    RSS_CONTENT = """
        <?xml version="1.0" encoding="utf-8"?>
        <rss version="2.0" xml:base="https://www.rss.mock"  xmlns:dc="http://purl.org/dc/elements/1.1/">
        <channel>
         <title>Mock Cybersecurity</title>
         <link>https://www.rss.mock</link>
         <description></description>
         <language>en</language>
        <item>
         <title>A Title</title>
         <link>https://www.rss.mock/a/url</link>
         <description>A word. hxxp://example.net/bad/another
         </description>
         <pubDate>Thu, 10 Oct 2017 17:00:00 +0000</pubDate>
         <dc:creator>Mock Testerman</dc:creator>
         <guid isPermaLink="false">1010 at https://www.rss.mock</guid>
        </item>
        <item>
         <title>Some Title</title>
         <link>https://www.rss.mock/some/url</link>
         <description>Some words. hxxp://example.com/bad/url
         </description>
         <pubDate>Thu, 01 Oct 2017 17:00:00 +0000</pubDate>
         <dc:creator>Mock Testerman</dc:creator>
         <guid isPermaLink="false">1000 at https://www.rss.mock</guid>
        </item>
        </channel>
        </rss>
    """

    def setUp(self):
        self.rss = sources.rss.RSS('http://rss.mock/rss.xml', 'messy')

    @httpretty.activate
    def test_smoke_rss_parsing(self):
        httpretty.register_uri(httpretty.GET, "http://rss.mock/rss.xml",
                body=self.RSS_CONTENT)

        saved_state, artifacts = self.rss.run(None)

        self.assertEquals(saved_state, u'Thu, 10 Oct 2017 17:00:00 +0000')
        self.assertEquals(len(artifacts), 4)
        self.assertIn('example.com', [str(x) for x in artifacts])
        self.assertIn('example.net', [str(x) for x in artifacts])
        self.assertIn('http://example.com/bad/url', [str(x) for x in artifacts])
        self.assertIn('http://example.net/bad/another', [str(x) for x in artifacts])
