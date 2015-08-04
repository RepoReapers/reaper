import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from lib import utilities
from tests import get_lsloc, REPOS_PATH


class CTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('C')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using GLib
        path = os.path.join(REPOS_PATH, 'gnome-vfs')
        proportion = self.discoverer.discover(path)
        self.assertLess(0, proportion)

        # Test: Project in Ruby to simulate a project with no C source code
        path = os.path.join(REPOS_PATH, 'squib')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_assert(self):
        # Test: Project using assert.h
        path = os.path.join(REPOS_PATH, 'http-parser')
        proportion = self.discoverer.__assert__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using assert.h
        path = os.path.join(REPOS_PATH, 'grs')
        proportion = self.discoverer.__assert__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_clar(self):
        # Test: Project using clar.h
        path = os.path.join(REPOS_PATH, 'libgit2')
        proportion = self.discoverer.__clar__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using clar.h
        path = os.path.join(REPOS_PATH, 'lwan')
        proportion = self.discoverer.__clar__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_glib(self):
        # Test: Project using GLib
        path = os.path.join(REPOS_PATH, 'gnome-vfs')
        proportion = self.discoverer.__glib__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using GLib
        path = os.path.join(REPOS_PATH, 'grs')
        proportion = self.discoverer.__glib__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_picotest(self):
        # Test: Project using Picotest
        path = os.path.join(REPOS_PATH, 'h2o')
        proportion = self.discoverer.__picotest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using Picotest
        path = os.path.join(REPOS_PATH, 'grs')
        proportion = self.discoverer.__picotest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)
