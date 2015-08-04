import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import get_lsloc, REPOS_PATH


class PhpTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('PHP')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using PHPUnit
        path = os.path.join(REPOS_PATH, 'composer')
        proportion = self.discoverer.discover(path)
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        path = os.path.join(REPOS_PATH, 'daux.io')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

        # Test: Project in Ruby to simulate a project with no C source code
        path = os.path.join(REPOS_PATH, 'squib')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_phpunit(self):
        # Test: Project using PHPUnit
        path = os.path.join(REPOS_PATH, 'composer')
        proportion = self.discoverer.__phpunit__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project using PHPUnit Database Extensions
        path = os.path.join(REPOS_PATH, 'microrest.php')
        proportion = self.discoverer.__phpunit__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using PHPUnit
        path = os.path.join(REPOS_PATH, 'laravel')
        proportion = self.discoverer.__phpunit__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)
