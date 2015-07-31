import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class RubyTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('Ruby')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using RSpec
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'squib')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'shenzhen')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_minitest(self):
        # Test: Project using Minitest
        proportion = self.discoverer.__minitest__(
            os.path.join(REPOS_PATH, 'linguist')
        )
        self.assertLess(0, proportion)

        proportion = self.discoverer.__minitest__(
            os.path.join(REPOS_PATH, 'docurium')
        )
        self.assertLess(0, proportion)

        # Test: Project not using Minitest
        proportion = self.discoverer.__minitest__(
            os.path.join(REPOS_PATH, 'ruby-git')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_rspec(self):
        # Test: Project using RSpec
        proportion = self.discoverer.__rspec__(
            os.path.join(REPOS_PATH, 'squib')
        )
        self.assertLess(0, proportion)

        # Test: Project not using RSpec
        proportion = self.discoverer.__rspec__(
            os.path.join(REPOS_PATH, 'ruby-git')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_ruby_unit_testing(self):
        # Test: Project using Ruby Unit Testing
        proportion = self.discoverer.__ruby_unit_testing__(
            os.path.join(REPOS_PATH, 'janky')
        )
        self.assertLess(0, proportion)

        # Test: Project not using Ruby Unit Testing
        proportion = self.discoverer.__ruby_unit_testing__(
            os.path.join(REPOS_PATH, 'squib')
        )
        self.assertEqual(0, proportion)
