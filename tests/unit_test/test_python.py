import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class PythonTestDiscovererTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_unittest(self):
        discoverer = get_test_discoverer('Python')

        # Test: Project using unittest
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'ansible')
        )
        self.assertLess(0, proportion)

        # Test: Project not using unittest
        proportion = discoverer.discover(
            os.path.join(REPOS_PATH, 'django-crispy-forms')
        )
        self.assertEqual(-1, proportion)
