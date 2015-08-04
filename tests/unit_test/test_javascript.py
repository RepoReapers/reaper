import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import get_lsloc, REPOS_PATH


class JavaScriptTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('JavaScript')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using Mocha
        path = os.path.join(REPOS_PATH, 'superagent')
        proportion = self.discoverer.discover(path)
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        path = os.path.join(REPOS_PATH, 'javascript')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

        # Test: Project in Ruby to simulate a project with no C source code
        path = os.path.join(REPOS_PATH, 'squib')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_mocha(self):
        # Test: Project using Mocha
        path = os.path.join(REPOS_PATH, 'superagent')
        proportion = self.discoverer.__mocha__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using Mocha
        path = os.path.join(REPOS_PATH, 'qunit')
        proportion = self.discoverer.__mocha__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)
