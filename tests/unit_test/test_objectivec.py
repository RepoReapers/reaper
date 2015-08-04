import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import get_lsloc, REPOS_PATH


class ObjectiveCTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('Objective-C')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using XCTest
        path = os.path.join(REPOS_PATH, 'Sparkle')
        proportion = self.discoverer.discover(path)
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        path = os.path.join(REPOS_PATH, 'MJExtension')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

        # Test: Project in Ruby to simulate a project with no C source code
        path = os.path.join(REPOS_PATH, 'squib')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_xctest(self):
        # Test: Project using XCTest
        path = os.path.join(REPOS_PATH, 'Sparkle')
        proportion = self.discoverer.__xctest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using XCTest
        path = os.path.join(REPOS_PATH, 'WebScraper-iOS')
        proportion = self.discoverer.__xctest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

        # Bug Fix Tests

        # Bug: If relative file paths in the input to utilities.loc() contained
        #   spaces then cloc would fail causing loc() to return None.
        path = os.path.join(
            REPOS_PATH, 'UITableViewController-Challenge-Solution'
        )
        proportion = self.discoverer.__xctest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)
