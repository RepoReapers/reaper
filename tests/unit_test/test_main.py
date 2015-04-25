import os
import unittest

from attributes.unit_test import main
from tests import REPOS_PATH


class MainTestCase(unittest.TestCase):
    def test_main(self):
        # Test: Project using Mocha
        self.assertTrue(main.run(
            0, os.path.join(REPOS_PATH, 'superagent'), MockCursor()
        ))

        # Test: Project with no unit tests (when these tests were written)
        self.assertFalse(main.run(
            0, os.path.join(REPOS_PATH, 'javascript'), MockCursor()
        ))


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
