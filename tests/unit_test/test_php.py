import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class PhpTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('PHP')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using PHPUnit
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'composer')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'daux.io')
        )
        self.assertIsNone(proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_phpunit(self):
        # Test: Project using PHPUnit
        proportion = self.discoverer.__phpunit__(
            os.path.join(REPOS_PATH, 'composer')
        )
        self.assertLess(0, proportion)

        # Test: Project using PHPUnit Database Extensions
        proportion = self.discoverer.__phpunit__(
            os.path.join(REPOS_PATH, 'microrest.php')
        )
        self.assertLess(0, proportion)

        # Test: Project not using PHPUnit
        proportion = self.discoverer.__phpunit__(
            os.path.join(REPOS_PATH, 'laravel')
        )
        self.assertIsNone(proportion)
