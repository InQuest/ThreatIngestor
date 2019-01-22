import unittest

from threatingestor.state import State


class TestState(unittest.TestCase):

    def setUp(self):
        self.state= State(":memory:")

    def test_state_updates_known_state(self):
        result = None
        initial= ["STATE","NAME"]
        expected = ["NEWSTATE","NAME"]

        #inital save state
        self.state.save_state(initial[1],initial[0])
        beforeUpdate = self.state.get_state(expected[1])

        #rewrite over same state
        self.state.save_state( expected[1], expected[0])
        afterUpdate= self.state.get_state(expected[1])

        self.assertEqual(afterUpdate, expected[0])

    def test_state_not_exists (self):
        result = None
        initial= ["STATE","NAME"]
        expected= None

        result= self.state.get_state(initial[1])

        self.assertEqual(result, expected)

    def test_state_saves(self):
        result = None
        expected = ["STATE","NAME"]
        self.state.save_state(expected[1],expected[0])

        result = self.state.get_state(expected[1])

        self.assertEqual(result, expected[0])
