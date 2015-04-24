import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class CSharpTestDiscovererTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        discoverer = get_test_discoverer('C#')

        # Test: Project using NUnit
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'choco')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'ShareX')
        )
        self.assertEqual(-1, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_nunit(self):
        discoverer = get_test_discoverer('C#')

        # Test: Project using NUnit
        proportion = discoverer.__nunit__(
            os.path.join(REPOS_PATH, 'choco')
        )
        self.assertLess(0, proportion)

        # Test: Project not using NUnit
        proportion = discoverer.__nunit__(
            os.path.join(REPOS_PATH, 'Epic.Numbers')
        )
        self.assertEqual(-1, proportion)
