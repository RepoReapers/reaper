import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import REPOS_PATH


class PythonTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('Python')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using RSpec
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'ansible')
        )
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        proportion = self.discoverer.discover(
            os.path.join(REPOS_PATH, 'curriculum')
        )
        self.assertIsNone(proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_django_test(self):
        # Test: Project using Django Test
        proportion = self.discoverer.__django_test__(
            os.path.join(REPOS_PATH, 'django-crispy-forms')
        )
        self.assertLess(0, proportion)

        # Test: Project not using Django Test
        proportion = self.discoverer.__django_test__(
            os.path.join(REPOS_PATH, 'ansible')
        )
        self.assertIsNone(proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_nose(self):
        # Test: Project using Nose Test
        proportion = self.discoverer.__nose__(
            os.path.join(REPOS_PATH, 'mbutil')
        )
        self.assertLess(0, proportion)

        # Test: Project not using Nose Test
        proportion = self.discoverer.__nose__(
            os.path.join(REPOS_PATH, 'django-crispy-forms')
        )
        self.assertIsNone(proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_unittest(self):
        # Test: Project using unittest
        proportion = self.discoverer.__unittest__(
            os.path.join(REPOS_PATH, 'ansible')
        )
        self.assertLess(0, proportion)

        # Test: Project not using unittest
        proportion = self.discoverer.__unittest__(
            os.path.join(REPOS_PATH, 'django-crispy-forms')
        )
        self.assertIsNone(proportion)
