import os
import unittest

from attributes.project_size import main
from tests import REPOS_PATH


class MainTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_main(self):
        (bresult, rresult) = main.run(
            0, os.path.join(REPOS_PATH, 'superagent'), MockCursor('js'),
            threshold=0
        )
        self.assertTrue(bresult)
        self.assertLessEqual(4300, rresult)

        (bresult, rresult) = main.run(
            0, os.path.join(REPOS_PATH, 'squib'), MockCursor('rb'),
            threshold=0
        )
        self.assertTrue(bresult)
        self.assertLessEqual(4525, rresult)

        (bresult, rresult) = main.run(
            0, os.path.join(REPOS_PATH, 'gnome-vfs'), MockCursor('c'),
            threshold=0
        )
        self.assertTrue(bresult)
        self.assertLessEqual(84542, rresult)


class MockCursor(object):
    def __init__(self, language):
        self.language = language

    def execute(self, string):
        pass

    def fetchone(self):
        if self.language == 'js':
            return ['JavaScript']
        elif self.language == 'c':
            return ['C']
        elif self.language == 'rb':
            return ['Ruby']

    def close(self):
        pass
