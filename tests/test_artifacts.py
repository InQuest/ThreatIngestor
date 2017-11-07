import unittest

import ipaddress

import artifacts

class TestArtifacts(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_unicode_support(self):
        self.assertEquals(type(artifacts.Artifact('test', 'test').__str__()), str)
        self.assertEquals(type(artifacts.Artifact('test', 'test').__unicode__()), unicode)
        self.assertEquals(type(artifacts.Artifact(u't\u1111st', 'test').__unicode__()), unicode)

    def test_url_ipv4(self):
        self.assertTrue(artifacts.URL('http://192.168.0.1', '').is_ipv4())
        self.assertTrue(artifacts.URL('http://192.168.0.1:80/path', '').is_ipv4())
        self.assertTrue(artifacts.URL('http://192[.]168[.]0[.]1:80/path', '').is_ipv4())
        self.assertTrue(artifacts.URL('192[.]168[.]0[.]1:80/path', '').is_ipv4())
        self.assertTrue(artifacts.URL('192.168.0.1', '').is_ipv4())
        self.assertTrue(artifacts.URL('tcp://192[.]168[.]0[.]1:80/path', '').is_ipv4())
        self.assertFalse(artifacts.URL('tcp://[fdc4:2581:575b:5a72:0000:0000:0000:0001]:80/path', '').is_ipv4())
        self.assertFalse(artifacts.URL('http://example.com:80/path', '').is_ipv4())

    def test_url_ipv6(self):
        self.assertTrue(artifacts.URL('http://fdc4:2581:575b:5a72:0000:0000:0000:0001', '').is_ipv6())
        self.assertTrue(artifacts.URL('http://[fdc4:2581:575b:5a72:0000:0000:0000:0001]:80/path', '').is_ipv6())
        self.assertTrue(artifacts.URL('[fdc4:2581:575b:5a72:0000:0000:0000:0001]:80/path', '').is_ipv6())
        self.assertTrue(artifacts.URL('fdc4:2581:575b:5a72:0000:0000:0000:0001', '').is_ipv6())
        self.assertTrue(artifacts.URL('tcp://[fdc4:2581:575b:5a72:0000:0000:0000:0001]:80/path', '').is_ipv6())
        self.assertFalse(artifacts.URL('tcp://192[.]168[.]0[.]1:80/path', '').is_ipv6())
        self.assertFalse(artifacts.URL('http://example.com:80/path', '').is_ipv6())

    def test_url_deobfuscation(self):
        self.assertEquals(artifacts.URL('http://example.com/', '').deobfuscated(), 'http://example.com/')
        self.assertEquals(artifacts.URL('http://example[.]com/', '').deobfuscated(), 'http://example.com/')
        self.assertEquals(artifacts.URL('http://example[.]com/[.]', '').deobfuscated(), 'http://example.com/[.]')
        self.assertEquals(artifacts.URL('hxxp://example[.]com/', '').deobfuscated(), 'http://example.com/')
        self.assertEquals(artifacts.URL('tcp://example[.]com/', '').deobfuscated(), 'http://example.com/')
        self.assertEquals(artifacts.URL('example[.]com/', '').deobfuscated(), 'http://example.com/')
        self.assertEquals(artifacts.URL('hxxp://example[dot]com/', '').deobfuscated(), 'http://example.com/')
        self.assertEquals(artifacts.URL('example[dot]com', '').deobfuscated(), 'http://example.com')
        self.assertEquals(artifacts.URL('192[.]168[dot]0[.]1', '').deobfuscated(), 'http://192.168.0.1')
        self.assertEquals(artifacts.URL('http://example[.com/', '').deobfuscated(), 'http://example.com/')
        self.assertEquals(artifacts.URL('http://example.com/ test', '').deobfuscated(), 'http://example.com/ test')
        self.assertEquals(artifacts.URL('http://example.com test /test', '').deobfuscated(), 'http://example.com/test')
        self.assertEquals(artifacts.URL('http://[fdc4:2581:575b:5a72:0000:0000:0000:0001]:80/path', '').deobfuscated(),
                                        'http://[fdc4:2581:575b:5a72:0000:0000:0000:0001]:80/path')
        self.assertEquals(artifacts.URL('http://example.com[/]test', '').deobfuscated(), 'http://example.com/test')
        self.assertEquals(artifacts.URL('http://[example.com', '').deobfuscated(), 'http://example.com')
        self.assertEquals(artifacts.URL(u'http://example\u30fbcom', '').deobfuscated(), 'http://example.com')

    def test_is_obfuscated(self):
        self.assertFalse(artifacts.URL('example.com', '').is_obfuscated())
        self.assertFalse(artifacts.URL('http://example.com', '').is_obfuscated())
        self.assertFalse(artifacts.URL('http://example.com/[.', '').is_obfuscated())
        self.assertFalse(artifacts.URL('http://192.168.0.1', '').is_obfuscated())
        self.assertFalse(artifacts.URL('192.168.0.1', '').is_obfuscated())
        self.assertTrue(artifacts.URL('hxxp://example.com', '').is_obfuscated())
        self.assertTrue(artifacts.URL('http://example[.]com', '').is_obfuscated())
        self.assertTrue(artifacts.URL('hxxp://example[.]com', '').is_obfuscated())
        self.assertTrue(artifacts.URL('example[.]com', '').is_obfuscated())
        self.assertTrue(artifacts.URL('http://example[dot]com', '').is_obfuscated())
        self.assertTrue(artifacts.URL('http://192[.]168[.]0[.]1', '').is_obfuscated())
        self.assertTrue(artifacts.URL('192[.]168[.]0[.]1', '').is_obfuscated())

    def test_url_domain_parsing(self):
        self.assertEquals(artifacts.URL('http://example.com/', '').domain(), 'example.com')
        self.assertEquals(artifacts.URL('http://example[.]com/', '').domain(), 'example.com')
        self.assertEquals(artifacts.URL('http://example[.]com/[.].com', '').domain(), 'example.com')
        self.assertEquals(artifacts.URL('tcp://example[.]com:80/', '').domain(), 'example.com')
        self.assertEquals(artifacts.URL('example[.]com/', '').domain(), 'example.com')
        self.assertEquals(artifacts.URL('example[.]com test', '').domain(), 'example.com')

    def test_ipaddress_parsing(self):
        # str
        self.assertEquals(str(artifacts.IPAddress('192[.]168[.]0[.]1', '')), '192.168.0.1')
        self.assertEquals(str(artifacts.IPAddress('192.168.0.1/some/url', '')), '192.168.0.1')
        self.assertEquals(str(artifacts.IPAddress('192.168.0.1:9090', '')), '192.168.0.1')
        self.assertEquals(str(artifacts.IPAddress('192.168.0.1:9090/url', '')), '192.168.0.1')
        self.assertEquals(str(artifacts.IPAddress('192[.]168[.]0[.]1:9090/url', '')), '192.168.0.1')
        self.assertNotEquals(str(artifacts.IPAddress('192[.]188[dot]0[.]1:9090/url', '')), '192.168.0.1')
        # ipaddress
        self.assertEquals(artifacts.IPAddress('192[.]168[.]0[.]1', '').ipaddress(), ipaddress.IPv4Address(u'192.168.0.1'))
        self.assertEquals(artifacts.IPAddress('192.168.0.1/some/url', '').ipaddress(), ipaddress.IPv4Address(u'192.168.0.1'))
        self.assertEquals(artifacts.IPAddress('192.168.0.1:9090', '').ipaddress(), ipaddress.IPv4Address(u'192.168.0.1'))
        self.assertEquals(artifacts.IPAddress('192.168.0.1:9090/url', '').ipaddress(), ipaddress.IPv4Address(u'192.168.0.1'))
        self.assertEquals(artifacts.IPAddress('192[.]168[.]0[.]1:9090/url', '').ipaddress(), ipaddress.IPv4Address(u'192.168.0.1'))
