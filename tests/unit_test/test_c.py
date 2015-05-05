import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class CTestDiscovererTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        discoverer = get_test_discoverer('C')

        # Test: Project using GLib
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'gnome-vfs')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'lwan')
        )
        self.assertEqual(-1, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_glib(self):
        discoverer = get_test_discoverer('C')

        # Test: Project using GLib
        proportion = discoverer.__glib__(
            os.path.join(REPOS_PATH, 'gnome-vfs')
        )
        self.assertLess(0, proportion)

        # Test: Project not using GLib
        proportion = discoverer.__glib__(
            os.path.join(REPOS_PATH, 'grs')
        )
        self.assertEqual(-1, proportion)
