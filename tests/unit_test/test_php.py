import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class PhpTestDiscovererTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        discoverer = get_test_discoverer('PHP')

        # Test: Project using PHPUnit
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'composer')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'daux.io')
        )
        self.assertEqual(-1, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_phpunit(self):
        discoverer = get_test_discoverer('PHP')

        # Test: Project using PHPUnit
        proportion = discoverer.__phpunit__(
            os.path.join(REPOS_PATH, 'composer')
        )
        self.assertLess(0, proportion)

        # Test: Project not using PHPUnit
        proportion = discoverer.__phpunit__(
            os.path.join(REPOS_PATH, 'laravel')
        )
        self.assertEqual(-1, proportion)
