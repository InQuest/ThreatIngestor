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
        self.assertTrue(artifacts.URL('http://192,168,0,1', '').is_ipv4())
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
        self.assertEquals(artifacts.URL('http://example(.)com/', '').deobfuscated(), 'http://example.com/')
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
        self.assertEquals(artifacts.URL('http://192,168,0,1', '').deobfuscated(), 'http://192.168.0.1')
        self.assertEquals(artifacts.URL('http://example,com/', '').deobfuscated(), 'http://example.com/')

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

    def test_is_domain(self):
        # valid
        self.assertTrue(artifacts.URL('example.com', '').is_domain())
        self.assertTrue(artifacts.URL('example,com', '').is_domain())
        self.assertTrue(artifacts.URL('http://example.com', '').is_domain())
        self.assertTrue(artifacts.URL('example[.]com', '').is_domain())
        self.assertTrue(artifacts.URL('http://example[dot]com', '').is_domain())
        self.assertTrue(artifacts.URL('http://exa-mple.com', '').is_domain())
        self.assertTrue(artifacts.URL('http://ex4mple.com', '').is_domain())
        self.assertTrue(artifacts.URL(u'http://example\u30fbcom', '').is_domain())
        self.assertTrue(artifacts.URL('short.is', '').is_domain())
        # invalid
        self.assertFalse(artifacts.URL('http://192[.]168[.]0[.]1', '').is_domain())
        self.assertFalse(artifacts.URL('192.168.0.1', '').is_domain())
        self.assertFalse(artifacts.URL('AAAAA', '').is_domain())
        self.assertFalse(artifacts.URL('+example.tld+', '').is_domain())
        self.assertFalse(artifacts.URL('85', '').is_domain())
        self.assertFalse(artifacts.URL('85.85', '').is_domain())
        self.assertFalse(artifacts.URL(u'exa\u30f2ple.com', '').is_domain())
        self.assertFalse(artifacts.URL('_____', '').is_domain())
        self.assertFalse(artifacts.URL('_____.tld', '').is_domain())
        self.assertFalse(artifacts.URL('http://example.com\\bad.doc', '').is_domain())
        self.assertFalse(artifacts.URL('x.x.x.x', '').is_domain())
        self.assertFalse(artifacts.URL('tooshor.t', '').is_domain())
        self.assertFalse(artifacts.URL('tooshor.', '').is_domain())

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

    def test_match_artifact_regex(self):
        self.assertTrue(artifacts.IPAddress('192.168.0.1', '').match('192'))
        self.assertTrue(artifacts.IPAddress('192.168.0.1', '').match('168'))
        self.assertTrue(artifacts.IPAddress('192.168.0.1', '').match('192\.168'))
        self.assertTrue(artifacts.IPAddress('192.168.0.1', '').match('.'))
        self.assertTrue(artifacts.IPAddress('192.168.0.1', '').match('\.'))
        self.assertTrue(artifacts.IPAddress('192.168.0.1', '').match('.*'))
        self.assertTrue(artifacts.IPAddress('192[.]168.0[.]1', '').match('^192\.168\.0\.1$'))
        self.assertFalse(artifacts.IPAddress('192.168.0.1', '').match('168.192'))
        self.assertFalse(artifacts.IPAddress('192.168.0.1', '').match('192.*2'))
        self.assertFalse(artifacts.IPAddress('192.168.0.1', '').match('test'))
        self.assertTrue(artifacts.URL('http://example[.com', '').match('example.com'))
        self.assertTrue(artifacts.URL('http://example[.com/test.doc', '').match('.*\.doc'))
        # empty always matches
        self.assertTrue(artifacts.IPAddress('192.168.0.1', '').match(''))

    def test_match_url_condition_expression(self):
        # should be treated as regex
        self.assertTrue(artifacts.URL('http://example[.com/test.doc', '').match('.*\.doc'))
        self.assertTrue(artifacts.URL('http://example[.com/not is_ip', '').match('not is_ip.*'))
        self.assertTrue(artifacts.URL('http://example[.com/not is_ip,', '').match('not is_ip,.*'))
        # should be treated as condition
        self.assertTrue(artifacts.URL('http://example[.com/not is_ip', '').match('not is_ip'))
        self.assertTrue(artifacts.URL('http://example[.com/not is_ip', '').match('is_domain'))
        self.assertTrue(artifacts.URL('http://example[.com/', '').match('is_domain'))
        self.assertTrue(artifacts.URL('http://example[.com/', '').match('is_domain, not is_ip'))

        self.assertFalse(artifacts.URL('http://example[.com/', '').match('is_ip'))
        self.assertFalse(artifacts.URL('http://example[.com/', '').match('is_ip, not is_domain'))

        # first element true
        self.assertFalse(artifacts.URL('http://example[.com/', '').match('not is_ip, not is_domain'))
        # second element true
        self.assertFalse(artifacts.URL('http://example[.com/', '').match('is_ip, is_domain'))

        self.assertTrue(artifacts.URL('http://192.168[.]0.1/test.doc', '').match('is_ip, not is_domain, is_ipv4'))
        self.assertTrue(artifacts.URL('http://[[2001:db8:85a3::8a2e:370:7334]]/test.doc', '').match('is_ip, not is_domain, is_ipv6, not is_ipv4'))
        self.assertTrue(artifacts.URL('http://example[.com/test.doc', '').match('is_obfuscated'))
        self.assertFalse(artifacts.URL('http://example.com/test.doc', '').match('is_obfuscated'))
        self.assertTrue(artifacts.URL('http://example.com/test.doc', '').match('not is_obfuscated, is_domain'))

        # empty always matches
        self.assertTrue(artifacts.URL('http://example.com/test.doc', '').match(''))
