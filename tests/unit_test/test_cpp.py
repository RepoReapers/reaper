import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class CppDiscovererTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_boost(self):
        discoverer = get_test_discoverer('C++')

        # Test: Project using Boost
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'externals-clasp')
        )
        self.assertLess(0, proportion)

        # Test: Project not using Boost
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'openage')
        )
        self.assertEqual(-1, proportion)
