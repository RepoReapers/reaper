import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class RubyTestDiscovererTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        discoverer = get_test_discoverer('Ruby')

        # Test: Project using RSpec
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'squib')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'shenzhen')
        )
        self.assertEqual(-1, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_rspec(self):
        discoverer = get_test_discoverer('Ruby')

        # Test: Project using RSpec
        proportion = discoverer.__rspec__(
            os.path.join(REPOS_PATH, 'squib')
        )
        self.assertLess(0, proportion)

        # Test: Project not using RSpec
        proportion = discoverer.__rspec__(
            os.path.join(REPOS_PATH, 'ruby-git')
        )
        self.assertEqual(-1, proportion)
