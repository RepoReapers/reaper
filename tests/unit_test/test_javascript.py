import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class JavaScriptTestDiscovererTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        discoverer = get_test_discoverer('JavaScript')

        # Test: Project using Mocha
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'superagent')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'javascript')
        )
        self.assertEqual(-1, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_mocha(self):
        discoverer = get_test_discoverer('JavaScript')

        # Test: Project using Mocha
        proportion = discoverer.__mocha__(
            os.path.join(REPOS_PATH, 'superagent')
        )
        self.assertLess(0, proportion)

        # Test: Project not using Mocha
        proportion = discoverer.__mocha__(
            os.path.join(REPOS_PATH, 'qunit')
        )
        self.assertEqual(-1, proportion)
