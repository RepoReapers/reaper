import os
import unittest

from attributes.unit_test import main
from tests import REPOS_PATH


class MainTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_main(self):
        # Test: Project using Mocha
        (result, value) = main.run(
            0, os.path.join(REPOS_PATH, 'superagent'), MockCursor(),
            threshold=0.1
        )
        self.assertTrue(result)
        self.assertLess(0, value)

        # Test: Project with no unit tests (when these tests were written)
        (result, value) = main.run(
            0, os.path.join(REPOS_PATH, 'javascript'), MockCursor(),
            threshold=0.1
        )
        self.assertFalse(result)
        self.assertEqual(0, value)

        # Test: Project in Ruby but database says JavaScript
        (result, value) = main.run(
            0, os.path.join(REPOS_PATH, 'squib'), MockCursor(), threshold=0.1
        )
        self.assertFalse(result)
        self.assertEqual(0, value)


class MockCursor(object):
    def __init__(self):
        super(MockCursor, self).__init__()
        self.record = None

    def execute(self, string):
        pass

    def fetchone(self):
        return ['JavaScript']

    def close(self):
        pass
