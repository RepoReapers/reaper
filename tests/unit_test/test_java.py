import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class JavaTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('Java')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using JUnit
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'maven')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'MPAndroidChart')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_junit(self):
        # Test: Project using JUnit
        proportion = self.discoverer.__junit__(
            os.path.join(REPOS_PATH, 'maven')
        )
        self.assertLess(0, proportion)

        # Test: Project using JUnit without mention in pom.xml
        proportion = self.discoverer.__junit__(
            os.path.join(REPOS_PATH, 'cassandra')
        )
        self.assertLess(0, proportion)

        # Test: Project not using JUnit
        proportion = self.discoverer.__junit__(
            os.path.join(REPOS_PATH, 'MPAndroidChart')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_testng(self):
        # Test: Project using TestNG
        proportion = self.discoverer.__testng__(
            os.path.join(REPOS_PATH, 'SimianArmy')
        )
        self.assertLess(0, proportion)

        # Test: Project not using TestNG
        proportion = self.discoverer.__testng__(
            os.path.join(REPOS_PATH, 'maven')
        )
        self.assertEqual(0, proportion)
