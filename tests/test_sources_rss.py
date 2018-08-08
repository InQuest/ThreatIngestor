import unittest

import httpretty

import threatingestor.sources.rss


class TestRSS(unittest.TestCase):

    RSS_CONTENT = """<?xml version="1.0" encoding="utf-8"?>
        <rss version="2.0" xml:base="https://www.rss.mock"  xmlns:dc="http://purl.org/dc/elements/1.1/">
        <channel>
         <title>Mock Cybersecurity</title>
         <link>https://www.rss.mock</link>
         <description></description>
         <language>en</language>
        <item>
         <title>Another Title</title>
         <link>https://www.rss.mock/some/url</link>
         <description>Some words. http://example.com/bad/url/30
         </description>
         <pubDate>Fri, 11 Oct 2017 17:00:00 +0000</pubDate>
         <dc:creator>Mock Testerman</dc:creator>
         <guid isPermaLink="false">1030 at https://www.rss.mock</guid>
        </item>
        <item>
         <title>A Title</title>
         <link>https://www.rss.mock/a/url</link>
         <description>A word. hxxp://example.net/bad/another/20
         </description>
         <pubDate>Thu, 10 Oct 2017 17:00:00 +0000</pubDate>
         <dc:creator>Mock Testerman</dc:creator>
         <guid isPermaLink="false">1020 at https://www.rss.mock</guid>
        </item>
        <item>
         <title>Some Title</title>
         <link>https://www.rss.mock/some/url</link>
         <content:encoded>Some words. hxxp://example<b>.</b>com/bad/url/10
         </content>
         <pubDate>Thu, 01 Oct 2017 17:00:00 +0000</pubDate>
         <dc:creator>Mock Testerman</dc:creator>
         <guid isPermaLink="false">1010 at https://www.rss.mock</guid>
        </item>
        <item>
         <title>No link</title>
         <description>Some words. http://example.com/good/url
         Indicators of Compromise
         http://example.com/bad/url/00
         </description>
         <pubDate>Wed, 30 Sep 2017 17:00:00 +0000</pubDate>
         <dc:creator>Mock Testerman</dc:creator>
         <guid isPermaLink="false">1000 at https://www.rss.mock</guid>
        </item>
        </channel>
        </rss>
    """

    def setUp(self):
        self.rss = threatingestor.sources.rss.Plugin('myrss', 'http://rss.mock/rss.xml', 'messy')

    @httpretty.activate
    def test_run_respects_saved_state(self):
        httpretty.register_uri(httpretty.GET, "http://rss.mock/rss.xml",
                body=self.RSS_CONTENT)

        # normal usage
        saved_state, artifacts = self.rss.run(None)
        self.assertEqual(len(artifacts), 8)
        saved_state, artifacts = self.rss.run(saved_state)
        self.assertEqual(len(artifacts), 0)

        # fake saved_state
        saved_state, artifacts = self.rss.run('Thu, 01 Oct 2017 17:00:00 +0000')
        self.assertEqual(len(artifacts), 4)

    @httpretty.activate
    def test_run_does_preprocessing_deobfuscation(self):
        httpretty.register_uri(httpretty.GET, "http://rss.mock/rss.xml",
                body=self.RSS_CONTENT)

        saved_state, artifacts = self.rss.run(None)

        # <b> tag obfuscation
        self.assertIn('http://example.com/bad/url/10', [str(x) for x in artifacts])

    @httpretty.activate
    def test_run_respects_feed_type(self):
        httpretty.register_uri(httpretty.GET, "http://rss.mock/rss.xml",
                body=self.RSS_CONTENT)

        messy = threatingestor.sources.rss.Plugin('myrss', 'http://rss.mock/rss.xml', 'messy')
        clean = threatingestor.sources.rss.Plugin('testrss', 'http://rss.mock/rss.xml', 'clean')
        afterioc = threatingestor.sources.rss.Plugin('rsss', 'http://rss.mock/rss.xml', 'afterioc')

        saved_state, artifacts = messy.run(None)
        self.assertEqual(len(artifacts), 8)
        self.assertIn('http://example.com/bad/url/10', [str(x) for x in artifacts])
        self.assertNotIn('http://example.com/good/url', [str(x) for x in artifacts])
        self.assertNotIn('http://example.com/bad/url/00', [str(x) for x in artifacts])

        saved_state, artifacts = clean.run(None)
        self.assertEqual(len(artifacts), 14)
        self.assertIn('http://example.com/bad/url/10', [str(x) for x in artifacts])
        self.assertIn('http://example.com/good/url', [str(x) for x in artifacts])
        self.assertIn('http://example.com/bad/url/00', [str(x) for x in artifacts])

        saved_state, artifacts = afterioc.run(None)
        self.assertEqual(len(artifacts), 12)
        self.assertIn('http://example.com/bad/url/10', [str(x) for x in artifacts])
        self.assertNotIn('http://example.com/good/url', [str(x) for x in artifacts])
        self.assertIn('http://example.com/bad/url/00', [str(x) for x in artifacts])

    @httpretty.activate
    def test_run_supports_both_content_summary(self):
        httpretty.register_uri(httpretty.GET, "http://rss.mock/rss.xml",
                body=self.RSS_CONTENT)

        saved_state, artifacts = self.rss.run(None)
        self.assertEqual(len(artifacts), 8)
        self.assertIn('http://example.com/bad/url/10', [str(x) for x in artifacts])
        self.assertIn('http://example.net/bad/another/20', [str(x) for x in artifacts])

    @httpretty.activate
    def test_run_supports_both_link_url(self):
        httpretty.register_uri(httpretty.GET, "http://rss.mock/rss.xml",
                body=self.RSS_CONTENT)

        saved_state, artifacts = self.rss.run(None)

        # link
        self.assertIn('http://example.com/bad/url/10', [str(x) for x in artifacts])
        self.assertIn('https://www.rss.mock/some/url', [a.reference_link for a in artifacts])

        afterioc = threatingestor.sources.rss.Plugin('test', 'http://rss.mock/rss.xml', 'afterioc')
        saved_state, artifacts = afterioc.run(None)

        # fallback to url
        self.assertIn('http://example.com/bad/url/00', [str(x) for x in artifacts])
        self.assertEqual(artifacts[0].reference_link, 'http://rss.mock/rss.xml')

    @httpretty.activate
    def test_run_returns_top_item_date_as_saved_state(self):
        httpretty.register_uri(httpretty.GET, "http://rss.mock/rss.xml",
                body=self.RSS_CONTENT)

        saved_state, artifacts = self.rss.run(None)

        self.assertEqual(saved_state, 'Fri, 11 Oct 2017 17:00:00 +0000')

    @httpretty.activate
    def test_run_returns_artifacts_correctly(self):
        httpretty.register_uri(httpretty.GET, "http://rss.mock/rss.xml",
                body=self.RSS_CONTENT)

        saved_state, artifacts = self.rss.run(None)

        self.assertEqual(saved_state, 'Fri, 11 Oct 2017 17:00:00 +0000')
        self.assertEqual(len(artifacts), 8)
        self.assertIn('example.com', [str(x) for x in artifacts])
        self.assertIn('example.net', [str(x) for x in artifacts])
        self.assertIn('http://example.com/bad/url/10', [str(x) for x in artifacts])
        self.assertIn('http://example.net/bad/another/20', [str(x) for x in artifacts])
