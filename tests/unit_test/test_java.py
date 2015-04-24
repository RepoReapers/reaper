import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class JavaTestDiscovererTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_junit(self):
        discoverer = get_test_discoverer('Java')

        # Test: Project using JUnit
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'maven')
        )
        self.assertLess(0, proportion)

        # Test: Project not using JUnit
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'SimianArmy')
        )
        self.assertEqual(-1, proportion)
