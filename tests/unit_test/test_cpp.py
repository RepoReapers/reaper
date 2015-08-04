import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import get_lsloc, REPOS_PATH


class CppTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('C++')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using Boost
        path = os.path.join(REPOS_PATH, 'externals-clasp')
        proportion = self.discoverer.discover(path)
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        path = os.path.join(REPOS_PATH, 'electron')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

        # Test: Project in Ruby to simulate a project with no C source code
        path = os.path.join(REPOS_PATH, 'squib')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_assert(self):
        # Test: Project using assert.h
        path = os.path.join(REPOS_PATH, 'IEDiagnosticsAdapter')
        proportion = self.discoverer.__assert__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using assert.h
        path = os.path.join(REPOS_PATH, 'electron')
        proportion = self.discoverer.__assert__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_boost(self):
        # Test: Project using Boost
        path = os.path.join(REPOS_PATH, 'externals-clasp')
        proportion = self.discoverer.__boost__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using Boost
        path = os.path.join(REPOS_PATH, 'openage')
        proportion = self.discoverer.__boost__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_catch(self):
        # Test: Project using Catch
        path = os.path.join(REPOS_PATH, 'variant')
        proportion = self.discoverer.__catch__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using Catch
        path = os.path.join(REPOS_PATH, 'electron')
        proportion = self.discoverer.__catch__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_gtest(self):
        # Test: Project using GTest
        path = os.path.join(REPOS_PATH, 'angle')
        proportion = self.discoverer.__gtest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using Gtest
        path = os.path.join(REPOS_PATH, 'electron')
        proportion = self.discoverer.__gtest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_stout_gtest(self):
        # Test: Project using Stout Gtest
        path = os.path.join(REPOS_PATH, 'mesos')
        proportion = self.discoverer.__stout_gtest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using Stout Gtest
        path = os.path.join(REPOS_PATH, 'electron')
        proportion = self.discoverer.__boost__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)
