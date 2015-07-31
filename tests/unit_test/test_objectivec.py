import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class ObjectiveCTestDiscovererTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        discoverer = get_test_discoverer('Objective-C')

        # Test: Project using XCTest
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'Sparkle')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'MJExtension')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_xctest(self):
        discoverer = get_test_discoverer('Objective-C')

        # Test: Project using XCTest
        proportion = discoverer.__xctest__(
            os.path.join(REPOS_PATH, 'Sparkle')
        )
        self.assertLess(0, proportion)

        # Test: Project not using XCTest
        proportion = discoverer.__xctest__(
            os.path.join(REPOS_PATH, 'WebScraper-iOS')
        )
        self.assertEqual(0, proportion)

        # Bug Fix Tests

        # Bug: If relative file paths in the input to utilities.loc() contained
        #   spaces then cloc would fail causing loc() to return None.
        proportion = discoverer.__xctest__(
            os.path.join(
                REPOS_PATH,
                'UITableViewController-Challenge-Solution'
            )
        )
        self.assertLess(0, proportion)
