import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class CSharpTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('C#')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using NUnit
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'choco')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'ShareX')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_nunit(self):
        # Test: Project using NUnit
        proportion = self.discoverer.__nunit__(
            os.path.join(REPOS_PATH, 'choco')
        )
        self.assertLess(0, proportion)

        # Test: Project not using NUnit
        proportion = self.discoverer.__nunit__(
            os.path.join(REPOS_PATH, 'Epic.Numbers')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_vs_unit_testing(self):
        # Test: Project using Visual Studio Unit Testing
        proportion = self.discoverer.__vs_unit_testing__(
            os.path.join(REPOS_PATH, 'aws-sdk-net')
        )
        self.assertLess(0, proportion)

        # Test: Project not using Visual Studio Unit Testing
        proportion = self.discoverer.__vs_unit_testing__(
            os.path.join(REPOS_PATH, 'choco')
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_xunit(self):
        # Test: Project using XUnit
        proportion = self.discoverer.__xunit__(
            os.path.join(REPOS_PATH, 'WebSockets')
        )
        self.assertLess(0, proportion)

        # Test: Project not using XUnit
        proportion = self.discoverer.__xunit__(
            os.path.join(REPOS_PATH, 'choco')
        )
        self.assertEqual(0, proportion)
