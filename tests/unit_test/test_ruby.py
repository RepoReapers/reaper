import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import get_lsloc, REPOS_PATH


class RubyTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('Ruby')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using RSpec
        path = os.path.join(REPOS_PATH, 'squib')
        proportion = self.discoverer.discover(path)
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        path = os.path.join(REPOS_PATH, 'shenzhen')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

        # Test: Project in C to simulate a project with no Ruby source code
        path = os.path.join(REPOS_PATH, 'gnome-vfs')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_minitest(self):
        # Test: Project using Minitest
        path = os.path.join(REPOS_PATH, 'linguist')
        proportion = self.discoverer.__minitest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        path = os.path.join(REPOS_PATH, 'docurium')
        proportion = self.discoverer.__minitest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using Minitest
        path = os.path.join(REPOS_PATH, 'ruby-git')
        proportion = self.discoverer.__minitest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_rspec(self):
        # Test: Project using RSpec
        path = os.path.join(REPOS_PATH, 'squib')
        proportion = self.discoverer.__rspec__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using RSpec
        path = os.path.join(REPOS_PATH, 'ruby-git')
        proportion = self.discoverer.__rspec__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_ruby_unit_testing(self):
        # Test: Project using Ruby Unit Testing
        path = os.path.join(REPOS_PATH, 'janky')
        proportion = self.discoverer.__ruby_unit_testing__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using Ruby Unit Testing
        path = os.path.join(REPOS_PATH, 'squib')
        proportion = self.discoverer.__ruby_unit_testing__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)
