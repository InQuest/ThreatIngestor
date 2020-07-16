import unittest
from pathlib import Path

from threatingestor.whitelist import Whitelist


class TestState(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).parent.absolute()
        path = parent / "fixtures/whitelist.json"
        self.whitelist = Whitelist(paths=[str(path)])

    def test_contains(self):
        self.assertTrue(self.whitelist.contains("00-tv.com"))
        self.assertFalse(self.whitelist.contains("example.com"))
