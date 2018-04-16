import unittest

import sources
import artifacts


class TestSources(unittest.TestCase):

    def setUp(self):
        # patch init
        self.orig_init = sources.Source.__init__
        sources.Source.__init__ = lambda x: None
        self.source = sources.Source()
        self.source.name = 'test'

    def tearDown(self):
        # unpatch init
        sources.Source.__init__ = self.orig_init

    def test_init_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.orig_init(self.source)

    def test_run_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.source.run(None)

    def test_truncate_length_is_respected(self):
        orig_truncate = sources.TRUNCATE_LENGTH
        sources.TRUNCATE_LENGTH = 15
        content = '123.45.67.89 0 12.33.45.67 890'

        artifact_list = self.source.process_element(content, 'link')
        self.assertEquals(artifact_list[0].reference_text, content[:15] + '...')

        sources.TRUNCATE_LENGTH = 8
        artifact_list = self.source.process_element(content, 'link')
        self.assertEquals(artifact_list[0].reference_text, content[:8] + '...')

        sources.TRUNCATE_LENGTH = orig_truncate

    def test_content_is_preprocessed(self):
        content = 'blah[.]com/test and test [.] com'

        artifact_list = self.source.process_element(content, 'link')
        self.assertIn('http://blah.com/test', [str(x) for x in artifact_list])
        self.assertIn('blah.com', [str(x) for x in artifact_list])
        self.assertIn('test.com', [str(x) for x in artifact_list])
        self.assertIn('http://test.com', [str(x) for x in artifact_list])
        self.assertEquals(len(artifact_list), 4)

    def test_urls_are_extracted(self):
        content = 'hxxp://someurl.com/test'

        artifact_list = self.source.process_element(content, 'link')
        self.assertEquals(str(artifact_list[0]), content.replace('xx', 'tt'))
        self.assertTrue(isinstance(artifact_list[0], artifacts.URL))
        self.assertEquals(str(artifact_list[1]), 'someurl.com')
        self.assertTrue(isinstance(artifact_list[1], artifacts.Domain))

    def test_ips_are_extracted(self):
        content = '232.23.21.12'

        artifact_list = self.source.process_element(content, 'link')
        self.assertEquals(str(artifact_list[0]), content)
        self.assertTrue(isinstance(artifact_list[0], artifacts.IPAddress))

    def test_yara_sigs_are_extracted(self):
        content = 'rule testRule { condition: true }'

        artifact_list = self.source.process_element(content, 'link')
        self.assertEquals(str(artifact_list[0]), content)
        self.assertTrue(isinstance(artifact_list[0], artifacts.YARASignature))

    def test_urls_matching_reference_link_are_discarded(self):
        content = 'hxxp://someurl.com/test hxxp://noturl.com/test'

        artifact_list = self.source.process_element(content, 'http://someurl.com')
        self.assertIn('http://noturl.com/test', [str(x) for x in artifact_list])
        self.assertIn('noturl.com', [str(x) for x in artifact_list])
        self.assertNotIn('http://someurl.com/test', [str(x) for x in artifact_list])
        self.assertNotIn('someurl.com', [str(x) for x in artifact_list])
        self.assertEquals(len(artifact_list), 2)

    def test_nonobfuscated_urls_are_discarded(self):
        content = 'hxxp://someurl.com/test http://noturl.com/test'

        artifact_list = self.source.process_element(content, 'link')
        self.assertNotIn('http://noturl.com/test', [str(x) for x in artifact_list])
        self.assertNotIn('noturl.com', [str(x) for x in artifact_list])
        self.assertIn('http://someurl.com/test', [str(x) for x in artifact_list])
        self.assertIn('someurl.com', [str(x) for x in artifact_list])
        self.assertEquals(len(artifact_list), 2)

    def test_nonobfuscated_urls_are_included_if_specified(self):
        content = 'hxxp://someurl.com/test http://noturl.com/test'

        artifact_list = self.source.process_element(content, 'link', include_nonobfuscated=True)
        self.assertIn('http://noturl.com/test', [str(x) for x in artifact_list])
        self.assertIn('noturl.com', [str(x) for x in artifact_list])
        self.assertIn('http://someurl.com/test', [str(x) for x in artifact_list])
        self.assertIn('someurl.com', [str(x) for x in artifact_list])
        self.assertEquals(len(artifact_list), 4)

    def test_source_name_is_included_in_artifacts(self):
        content = 'hxxp://someurl.com/test http://noturl.com/test'

        artifact_list = self.source.process_element(content, 'link')
        self.assertEquals(len(artifact_list), 2)
        self.assertEquals(artifact_list[0].source_name, 'test')
        self.assertEquals(artifact_list[1].source_name, 'test')
