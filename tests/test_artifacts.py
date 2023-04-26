import unittest

import ipaddress

import threatingestor.artifacts

class TestArtifacts(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_unicode_support(self):
        self.assertEqual(type(threatingestor.artifacts.Artifact('test', 'test').__str__()), str)
        self.assertEqual(type(threatingestor.artifacts.Artifact(u't\u1111st', 'test').__str__()), str)

    def test_url_ipv4(self):
        self.assertTrue(threatingestor.artifacts.URL('http://192.168.0.1', '').is_ipv4())
        self.assertTrue(threatingestor.artifacts.URL('http://192,168,0,1', '').is_ipv4())
        self.assertTrue(threatingestor.artifacts.URL('http://192.168.0.1:80/path', '').is_ipv4())
        self.assertTrue(threatingestor.artifacts.URL('http://192[.]168[.]0[.]1:80/path', '').is_ipv4())
        self.assertTrue(threatingestor.artifacts.URL('192[.]168[.]0[.]1:80/path', '').is_ipv4())
        self.assertTrue(threatingestor.artifacts.URL('192.168.0.1', '').is_ipv4())
        self.assertTrue(threatingestor.artifacts.URL('tcp://192[.]168[.]0[.]1:80/path', '').is_ipv4())
        self.assertFalse(threatingestor.artifacts.URL('tcp://[fdc4:2581:575b:5a72:0000:0000:0000:0001]:80/path', '').is_ipv4())
        self.assertFalse(threatingestor.artifacts.URL('http://example.com:80/path', '').is_ipv4())

    def test_url_ipv6(self):
        self.assertTrue(threatingestor.artifacts.URL('http://fdc4:2581:575b:5a72:0000:0000:0000:0001', '').is_ipv6())
        self.assertTrue(threatingestor.artifacts.URL('http://[fdc4:2581:575b:5a72:0000:0000:0000:0001]:80/path', '').is_ipv6())
        self.assertTrue(threatingestor.artifacts.URL('[fdc4:2581:575b:5a72:0000:0000:0000:0001]:80/path', '').is_ipv6())
        self.assertFalse(threatingestor.artifacts.URL('fdc4:2581:575b:5a72:0000:0000:0000:0001', '').is_ipv6())
        self.assertTrue(threatingestor.artifacts.URL('tcp://[fdc4:2581:575b:5a72:0000:0000:0000:0001]:80/path', '').is_ipv6())
        self.assertFalse(threatingestor.artifacts.URL('tcp://192[.]168[.]0[.]1:80/path', '').is_ipv6())
        self.assertFalse(threatingestor.artifacts.URL('http://example.com:80/path', '').is_ipv6())

    def test_url_deobfuscation(self):
        self.assertEqual(threatingestor.artifacts.URL('http://example.com/', '').deobfuscated(), 'http://example.com/')
        self.assertEqual(threatingestor.artifacts.URL('http://example[.]com/', '').deobfuscated(), 'http://example.com/')
        self.assertEqual(threatingestor.artifacts.URL('http://example(.)com/', '').deobfuscated(), 'http://example.com/')
        self.assertEqual(threatingestor.artifacts.URL('hxxp://example[.]com/', '').deobfuscated(), 'http://example.com/')
        self.assertEqual(threatingestor.artifacts.URL('tcp://example[.]com/', '').deobfuscated(), 'http://example.com/')
        self.assertEqual(threatingestor.artifacts.URL('example[.]com/', '').deobfuscated(), 'http://example.com/')
        self.assertEqual(threatingestor.artifacts.URL('hxxp://example[dot]com/', '').deobfuscated(), 'http://example.com/')
        self.assertEqual(threatingestor.artifacts.URL('example[dot]com', '').deobfuscated(), 'http://example.com')
        self.assertEqual(threatingestor.artifacts.URL('192[.]168[dot]0[.]1', '').deobfuscated(), 'http://192.168.0.1')
        self.assertEqual(threatingestor.artifacts.URL('http://example[.com/', '').deobfuscated(), 'http://example.com/')
        self.assertEqual(threatingestor.artifacts.URL('http://example.com/ test', '').deobfuscated(), 'http://example.com/ test')
        self.assertEqual(threatingestor.artifacts.URL('http://[fdc4:2581:575b:5a72:0000:0000:0000:0001]:80/path', '').deobfuscated(),
                                        'http://[fdc4:2581:575b:5a72:0000:0000:0000:0001]:80/path')
        self.assertEqual(threatingestor.artifacts.URL('http://example.com[/]test', '').deobfuscated(), 'http://example.com/test')
        self.assertEqual(threatingestor.artifacts.URL('http://[example.com', '').deobfuscated(), 'http://example.com')
        self.assertEqual(threatingestor.artifacts.URL(u'http://example\u30fbcom', '').deobfuscated(), 'http://example.com')
        self.assertEqual(threatingestor.artifacts.URL('http://192,168,0,1', '').deobfuscated(), 'http://192.168.0.1')
        self.assertEqual(threatingestor.artifacts.URL('http://example,com/', '').deobfuscated(), 'http://example.com/')

    def test_is_obfuscated(self):
        self.assertFalse(threatingestor.artifacts.URL('example.com', '').is_obfuscated())
        self.assertFalse(threatingestor.artifacts.URL('http://example.com', '').is_obfuscated())
        self.assertFalse(threatingestor.artifacts.URL('http://example.com/[', '').is_obfuscated())
        self.assertFalse(threatingestor.artifacts.URL('http://192.168.0.1', '').is_obfuscated())
        self.assertFalse(threatingestor.artifacts.URL('192.168.0.1', '').is_obfuscated())
        self.assertTrue(threatingestor.artifacts.URL('hxxp://example.com', '').is_obfuscated())
        self.assertTrue(threatingestor.artifacts.URL('http://example[.]com', '').is_obfuscated())
        self.assertTrue(threatingestor.artifacts.URL('hxxp://example[.]com', '').is_obfuscated())
        self.assertTrue(threatingestor.artifacts.URL('example[.]com', '').is_obfuscated())
        self.assertTrue(threatingestor.artifacts.URL('http://example[dot]com', '').is_obfuscated())
        self.assertTrue(threatingestor.artifacts.URL('http://192[.]168[.]0[.]1', '').is_obfuscated())
        self.assertTrue(threatingestor.artifacts.URL('192[.]168[.]0[.]1', '').is_obfuscated())

    def test_is_domain(self):
        # valid
        self.assertTrue(threatingestor.artifacts.URL('example.com', '').is_domain())
        self.assertTrue(threatingestor.artifacts.URL('example,com', '').is_domain())
        self.assertTrue(threatingestor.artifacts.URL('http://example.com', '').is_domain())
        self.assertTrue(threatingestor.artifacts.URL('example[.]com', '').is_domain())
        self.assertTrue(threatingestor.artifacts.URL('http://example[dot]com', '').is_domain())
        self.assertTrue(threatingestor.artifacts.URL('http://exa-mple.com', '').is_domain())
        self.assertTrue(threatingestor.artifacts.URL('http://ex4mple.com', '').is_domain())
        self.assertTrue(threatingestor.artifacts.URL(u'http://example\u30fbcom', '').is_domain())
        self.assertTrue(threatingestor.artifacts.URL('short.is', '').is_domain())
        # invalid
        self.assertFalse(threatingestor.artifacts.URL('http://192[.]168[.]0[.]1', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL('192.168.0.1', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL('AAAAA', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL('+example.tld+', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL('85', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL('85.85', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL(u'exa\u30f2ple.com', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL('_____', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL('_____.tld', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL('http://example.com\\bad.doc', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL('x.x.x.x', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL('tooshor.t', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL('tooshor.', '').is_domain())
        self.assertFalse(threatingestor.artifacts.URL('http://123.123.123.123/test', '').is_domain())

    def test_url_domain_parsing(self):
        self.assertEqual(threatingestor.artifacts.URL('http://example.com/', '').domain(), 'example.com')
        self.assertEqual(threatingestor.artifacts.URL('http://example[.]com/', '').domain(), 'example.com')
        self.assertEqual(threatingestor.artifacts.URL('http://example[.]com/[.].com', '').domain(), 'example.com')
        self.assertEqual(threatingestor.artifacts.URL('tcp://example[.]com:80/', '').domain(), 'example.com')
        self.assertEqual(threatingestor.artifacts.URL('example[.]com/', '').domain(), 'example.com')

    def test_ipaddress_parsing(self):
        # str
        self.assertEqual(str(threatingestor.artifacts.IPAddress('192[.]168[.]0[.]1', '')), '192.168.0.1')
        self.assertEqual(str(threatingestor.artifacts.IPAddress('192.168.0.1/some/url', '')), '192.168.0.1')
        self.assertEqual(str(threatingestor.artifacts.IPAddress('192.168.0.1:9090', '')), '192.168.0.1')
        self.assertEqual(str(threatingestor.artifacts.IPAddress('192.168.0.1:9090/url', '')), '192.168.0.1')
        self.assertEqual(str(threatingestor.artifacts.IPAddress('192[.]168[.]0[.]1:9090/url', '')), '192.168.0.1')
        self.assertNotEquals(str(threatingestor.artifacts.IPAddress('192[.]188[dot]0[.]1:9090/url', '')), '192.168.0.1')
        # ipaddress
        self.assertEqual(threatingestor.artifacts.IPAddress('192[.]168[.]0[.]1', '').ipaddress(), ipaddress.IPv4Address(u'192.168.0.1'))
        self.assertEqual(threatingestor.artifacts.IPAddress('192.168.0.1/some/url', '').ipaddress(), ipaddress.IPv4Address(u'192.168.0.1'))
        self.assertEqual(threatingestor.artifacts.IPAddress('192.168.0.1:9090', '').ipaddress(), ipaddress.IPv4Address(u'192.168.0.1'))
        self.assertEqual(threatingestor.artifacts.IPAddress('192.168.0.1:9090/url', '').ipaddress(), ipaddress.IPv4Address(u'192.168.0.1'))
        self.assertEqual(threatingestor.artifacts.IPAddress('192[.]168[.]0[.]1:9090/url', '').ipaddress(), ipaddress.IPv4Address(u'192.168.0.1'))

    def test_match_artifact_regex(self):
        self.assertTrue(threatingestor.artifacts.IPAddress('192.168.0.1', '').match('192'))
        self.assertTrue(threatingestor.artifacts.IPAddress('192.168.0.1', '').match('168'))
        self.assertTrue(threatingestor.artifacts.IPAddress('192.168.0.1', '').match('192\.168'))
        self.assertTrue(threatingestor.artifacts.IPAddress('192.168.0.1', '').match('.'))
        self.assertTrue(threatingestor.artifacts.IPAddress('192.168.0.1', '').match('\.'))
        self.assertTrue(threatingestor.artifacts.IPAddress('192.168.0.1', '').match('.*'))
        self.assertTrue(threatingestor.artifacts.IPAddress('192[.]168.0[.]1', '').match('^192\.168\.0\.1$'))
        self.assertFalse(threatingestor.artifacts.IPAddress('192.168.0.1', '').match('168.192'))
        self.assertFalse(threatingestor.artifacts.IPAddress('192.168.0.1', '').match('192.*2'))
        self.assertFalse(threatingestor.artifacts.IPAddress('192.168.0.1', '').match('test'))
        self.assertTrue(threatingestor.artifacts.URL('http://example[.com', '').match('example.com'))
        self.assertTrue(threatingestor.artifacts.URL('http://example[.com/test.doc', '').match('.*\.doc'))
        # empty always matches
        self.assertTrue(threatingestor.artifacts.IPAddress('192.168.0.1', '').match(''))

    def test_match_url_condition_expression(self):
        # should be treated as regex
        self.assertTrue(threatingestor.artifacts.URL('http://example[.com/test.doc', '').match('.*\.doc'))
        self.assertTrue(threatingestor.artifacts.URL('http://example[.com/not is_ip', '').match('not is_ip.*'))
        self.assertTrue(threatingestor.artifacts.URL('http://example[.com/not is_ip,', '').match('not is_ip,.*'))
        # should be treated as condition
        self.assertTrue(threatingestor.artifacts.URL('http://example[.com/not is_ip', '').match('not is_ip'))
        self.assertTrue(threatingestor.artifacts.URL('http://example[.com/not is_ip', '').match('is_domain'))
        self.assertTrue(threatingestor.artifacts.URL('http://example[.com/', '').match('is_domain'))
        self.assertTrue(threatingestor.artifacts.URL('http://example[.com/', '').match('is_domain, not is_ip'))

        self.assertFalse(threatingestor.artifacts.URL('http://example[.com/', '').match('is_ip'))
        self.assertFalse(threatingestor.artifacts.URL('http://example[.com/', '').match('is_ip, not is_domain'))

        # first element true
        self.assertFalse(threatingestor.artifacts.URL('http://example[.com/', '').match('not is_ip, not is_domain'))
        # second element true
        self.assertFalse(threatingestor.artifacts.URL('http://example[.com/', '').match('is_ip, is_domain'))

        self.assertTrue(threatingestor.artifacts.URL('http://192.168[.]0.1/test.doc', '').match('is_ip, not is_domain, is_ipv4'))
        self.assertTrue(threatingestor.artifacts.URL('http://[[2001:db8:85a3::8a2e:370:7334]]/test.doc', '').match('is_ip, not is_domain, is_ipv6, not is_ipv4'))
        self.assertTrue(threatingestor.artifacts.URL('http://example[.com/test.doc', '').match('is_obfuscated'))
        self.assertFalse(threatingestor.artifacts.URL('http://example.com/test.doc', '').match('is_obfuscated'))
        self.assertTrue(threatingestor.artifacts.URL('http://example.com/test.doc', '').match('not is_obfuscated, is_domain'))

        # empty always matches
        self.assertTrue(threatingestor.artifacts.URL('http://example.com/test.doc', '').match(''))

    def test_second_arg_to_artifact_is_source_name(self):
        self.assertEqual(threatingestor.artifacts.URL('http://t.co/', 'a').source_name, 'a')
        self.assertEqual(threatingestor.artifacts.Domain('t.co', 'a').source_name, 'a')

    def test_hash_type_is_correct(self):
        self.assertEqual(threatingestor.artifacts.Hash('68b329da9893e34099c7d8ad5cb9c940', '').hash_type(), threatingestor.artifacts.Hash.MD5)
        self.assertEqual(threatingestor.artifacts.Hash('adc83b19e793491b1c6ea0fd8b46cd9f32e592fc', '').hash_type(), threatingestor.artifacts.Hash.SHA1)
        self.assertEqual(threatingestor.artifacts.Hash('01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b', '').hash_type(),
                          threatingestor.artifacts.Hash.SHA256)
        self.assertEqual(threatingestor.artifacts.Hash('be688838ca8686e5c90689bf2ab585cef1137c999b48c70b92f67a5c34dc15697b5d11c982ed6d71be1e1e7f7b4e0733884aa97c3f7a339a8ed03577cf74be09', '').hash_type(),
                          threatingestor.artifacts.Hash.SHA512)
        self.assertEqual(threatingestor.artifacts.Hash('adc83b191b1c6ea0fd8b46cd9f32e592fc', '').hash_type(), None)

    def test_artifact_format_message(self):
        artifact = threatingestor.artifacts.Artifact('test', '', 'link', 'text')
        message = '{artifact}: "{reference_text}" -- {reference_link}'
        expected = 'test: "text" -- link'
        self.assertEqual(artifact.format_message(message), expected)

    def test_url_format_message(self):
        artifact = threatingestor.artifacts.URL('http://example.com/', '', 'link', 'text')
        message = '{artifact}: "{reference_text}" -- {reference_link}'
        expected = 'http://example.com/: "text" -- link'
        self.assertEqual(artifact.format_message(message), expected)

        artifact = threatingestor.artifacts.URL('http://example.com/', '', 'link', 'text')
        message = '{url} ({domain})'
        expected = 'http://example.com/ (example.com)'
        self.assertEqual(artifact.format_message(message), expected)

    def test_domain_format_message(self):
        artifact = threatingestor.artifacts.Domain('example.com', '', 'link', 'text')
        message = '{artifact}: "{reference_text}" -- {reference_link}'
        expected = 'example.com: "text" -- link'
        self.assertEqual(artifact.format_message(message), expected)

        artifact = threatingestor.artifacts.Domain('example.com', '', 'link', 'text')
        message = '({domain})'
        expected = '(example.com)'
        self.assertEqual(artifact.format_message(message), expected)

    def test_ipaddress_format_message(self):
        artifact = threatingestor.artifacts.IPAddress('1.1.1.1', '', 'link', 'text')
        message = '{artifact}: "{reference_text}" -- {reference_link}'
        expected = '1.1.1.1: "text" -- link'
        self.assertEqual(artifact.format_message(message), expected)

        artifact = threatingestor.artifacts.IPAddress('1.1.1.1', '', 'link', 'text')
        message = '({ipaddress})'
        expected = '(1.1.1.1)'
        self.assertEqual(artifact.format_message(message), expected)

    def test_hash_format_message(self):
        artifact = threatingestor.artifacts.Hash('test', '', 'link', 'text')
        message = '{artifact}: "{reference_text}" -- {reference_link}'
        expected = 'test: "text" -- link'
        self.assertEqual(artifact.format_message(message), expected)

        artifact = threatingestor.artifacts.Hash('68b329da9893e34099c7d8ad5cb9c940', '', 'link', 'text')
        message = '{hash_type}: {hash}'
        expected = 'md5: 68b329da9893e34099c7d8ad5cb9c940'
        self.assertEqual(artifact.format_message(message), expected)

        artifact = threatingestor.artifacts.Hash('1231231', '', 'link', 'text')
        message = '{hash_type}: {hash}'
        expected = 'hash: 1231231'
        self.assertEqual(artifact.format_message(message), expected)

    def test_yarasignature_format_message(self):
        artifact = threatingestor.artifacts.YARASignature('test', '', 'link', 'text')
        message = '{artifact}: "{reference_text}" -- {reference_link}'
        expected = 'test: "text" -- link'
        self.assertEqual(artifact.format_message(message), expected)

        artifact = threatingestor.artifacts.YARASignature('test', '', 'link', 'text')
        message = '{yarasignature}'
        expected = 'test'
        self.assertEqual(artifact.format_message(message), expected)

    def test_task_format_message(self):
        artifact = threatingestor.artifacts.Task('test', '', 'link', 'text')
        message = '{artifact}: "{reference_text}" -- {reference_link}'
        expected = 'test: "text" -- link'
        self.assertEqual(artifact.format_message(message), expected)

        artifact = threatingestor.artifacts.Task('test', '', 'link', 'text')
        message = '{task}: {reference_link}'
        expected = 'test: link'
        self.assertEqual(artifact.format_message(message), expected)

    def test_defanged_format_message(self):
        artifact = threatingestor.artifacts.URL('http://example.com/', '', 'link', 'text')
        message = '{defanged}'
        expected = 'hxxp://example[.]com/'
        self.assertEqual(artifact.format_message(message), expected)

        artifact = threatingestor.artifacts.Domain('example.com', '', 'link', 'text')
        message = '{defanged}'
        expected = 'example[.]com'
        self.assertEqual(artifact.format_message(message), expected)

        artifact = threatingestor.artifacts.IPAddress('1.1.1.1', '', 'link', 'text')
        message = '{defanged}'
        expected = '1[.]1[.]1[.]1'
        self.assertEqual(artifact.format_message(message), expected)
