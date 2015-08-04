import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import get_lsloc, REPOS_PATH


class JavaTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('Java')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using JUnit
        path = os.path.join(REPOS_PATH, 'maven')
        proportion = self.discoverer.discover(path)
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        path = os.path.join(REPOS_PATH, 'MPAndroidChart')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

        # Test: Project in Ruby to simulate a project with no C source code
        path = os.path.join(REPOS_PATH, 'squib')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_junit(self):
        # Test: Project using JUnit
        path = os.path.join(REPOS_PATH, 'maven')
        proportion = self.discoverer.__junit__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project using JUnit without mention in pom.xml
        path = os.path.join(REPOS_PATH, 'cassandra')
        proportion = self.discoverer.__junit__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using JUnit
        path = os.path.join(REPOS_PATH, 'MPAndroidChart')
        proportion = self.discoverer.__junit__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_testng(self):
        # Test: Project using TestNG
        path = os.path.join(REPOS_PATH, 'SimianArmy')
        proportion = self.discoverer.__testng__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using TestNG
        path = os.path.join(REPOS_PATH, 'maven')
        proportion = self.discoverer.__testng__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)
