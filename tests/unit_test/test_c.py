import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class CTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('C')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using GLib
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'gnome-vfs')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'grs')
        )
        self.assertIsNone(proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_assert(self):
        # Test: Project using assert.h
        proportion = self.discoverer.__assert__(
            os.path.join(REPOS_PATH, 'http-parser')
        )
        self.assertLess(0, proportion)

        # Test: Project not using assert.h
        proportion = self.discoverer.__assert__(
            os.path.join(REPOS_PATH, 'grs')
        )
        self.assertIsNone(proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_clar(self):
        # Test: Project using clar.h
        proportion = self.discoverer.__clar__(
            os.path.join(REPOS_PATH, 'libgit2')
        )
        self.assertLess(0, proportion)

        # Test: Project not using clar.h
        proportion = self.discoverer.__clar__(
            os.path.join(REPOS_PATH, 'lwan')
        )
        self.assertIsNone(proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_glib(self):
        # Test: Project using GLib
        proportion = self.discoverer.__glib__(
            os.path.join(REPOS_PATH, 'gnome-vfs')
        )
        self.assertLess(0, proportion)

        # Test: Project not using GLib
        proportion = self.discoverer.__glib__(
            os.path.join(REPOS_PATH, 'grs')
        )
        self.assertIsNone(proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_picotest(self):
        # Test: Project using Picotest
        proportion = self.discoverer.__picotest__(
            os.path.join(REPOS_PATH, 'h2o')
        )
        self.assertLess(0, proportion)

        # Test: Project not using Picotest
        proportion = self.discoverer.__picotest__(
            os.path.join(REPOS_PATH, 'grs')
        )
        self.assertIsNone(proportion)
