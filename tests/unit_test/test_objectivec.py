import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class ObjectiveCDiscovererTestCase(unittest.TestCase):
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
        self.assertEqual(-1, proportion)

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
        self.assertEqual(-1, proportion)
