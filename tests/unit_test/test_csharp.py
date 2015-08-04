import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import get_lsloc, REPOS_PATH


class CSharpTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('C#')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using NUnit
        path = os.path.join(REPOS_PATH, 'choco')
        proportion = self.discoverer.discover(path)
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        path = os.path.join(REPOS_PATH, 'ShareX')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

        # Test: Project in Ruby to simulate a project with no C source code
        path = os.path.join(REPOS_PATH, 'squib')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_nunit(self):
        # Test: Project using NUnit
        path = os.path.join(REPOS_PATH, 'choco')
        proportion = self.discoverer.__nunit__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using NUnit
        path = os.path.join(REPOS_PATH, 'Epic.Numbers')
        proportion = self.discoverer.__nunit__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_vs_unit_testing(self):
        # Test: Project using Visual Studio Unit Testing
        path = os.path.join(REPOS_PATH, 'aws-sdk-net')
        proportion = self.discoverer.__vs_unit_testing__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using Visual Studio Unit Testing
        path = os.path.join(REPOS_PATH, 'choco')
        proportion = self.discoverer.__vs_unit_testing__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_xunit(self):
        # Test: Project using XUnit
        path = os.path.join(REPOS_PATH, 'WebSockets')
        proportion = self.discoverer.__xunit__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using XUnit
        path = os.path.join(REPOS_PATH, 'choco')
        proportion = self.discoverer.__xunit__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)
