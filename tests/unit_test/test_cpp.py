import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class CppTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('C++')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using Boost
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'externals-clasp')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'electron')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_assert(self):
        # Test: Project using assert.h
        proportion = self.discoverer.__assert__(
            os.path.join(REPOS_PATH, 'IEDiagnosticsAdapter')
        )
        self.assertLess(0, proportion)

        # Test: Project not using assert.h
        proportion = self.discoverer.__assert__(
            os.path.join(REPOS_PATH, 'electron')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_boost(self):
        # Test: Project using Boost
        proportion = self.discoverer.__boost__(
            os.path.join(REPOS_PATH, 'externals-clasp')
        )
        self.assertLess(0, proportion)

        # Test: Project not using Boost
        proportion = self.discoverer.__boost__(
            os.path.join(REPOS_PATH, 'openage')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_catch(self):
        # Test: Project using Catch
        proportion = self.discoverer.__catch__(
            os.path.join(REPOS_PATH, 'variant')
        )
        self.assertLess(0, proportion)

        # Test: Project not using Catch
        proportion = self.discoverer.__catch__(
            os.path.join(REPOS_PATH, 'electron')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_gtest(self):
        # Test: Project using GTest
        proportion = self.discoverer.__gtest__(
            os.path.join(REPOS_PATH, 'angle')
        )
        self.assertLess(0, proportion)

        # Test: Project not using Gtest
        proportion = self.discoverer.__gtest__(
            os.path.join(REPOS_PATH, 'electron')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_stout_gtest(self):
        # Test: Project using Stout Gtest
        proportion = self.discoverer.__stout_gtest__(
            os.path.join(REPOS_PATH, 'mesos')
        )
        self.assertLess(0, proportion)

        # Test: Project not using Stout Gtest
        proportion = self.discoverer.__boost__(
            os.path.join(REPOS_PATH, 'electron')
        )
        self.assertEqual(0, proportion)
