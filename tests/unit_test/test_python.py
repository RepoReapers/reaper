import os
import unittest

from attributes.unit_test.discoverer import get_test_discoverer
from tests import get_lsloc, REPOS_PATH


class PythonTestDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.discoverer = get_test_discoverer('Python')

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Project using RSpec
        path = os.path.join(REPOS_PATH, 'ansible')
        proportion = self.discoverer.discover(path)
        self.assertLess(0, proportion)

        # Test: Project with no unit tests (when these tests were written)
        path = os.path.join(REPOS_PATH, 'curriculum')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

        # Test: Project in Ruby to simulate a project with no C source code
        path = os.path.join(REPOS_PATH, 'squib')
        proportion = self.discoverer.discover(path)
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_django_test(self):
        # Test: Project using Django Test
        path = os.path.join(REPOS_PATH, 'django-crispy-forms')
        proportion = self.discoverer.__django_test__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using Django Test
        path = os.path.join(REPOS_PATH, 'ansible')
        proportion = self.discoverer.__django_test__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_nose(self):
        # Test: Project using Nose Test
        path = os.path.join(REPOS_PATH, 'mbutil')
        proportion = self.discoverer.__nose__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using Nose Test
        path = os.path.join(REPOS_PATH, 'django-crispy-forms')
        proportion = self.discoverer.__nose__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_unittest(self):
        # Test: Project using unittest
        path = os.path.join(REPOS_PATH, 'ansible')
        proportion = self.discoverer.__unittest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertLess(0, proportion)

        # Test: Project not using unittest
        path = os.path.join(REPOS_PATH, 'django-crispy-forms')
        proportion = self.discoverer.__unittest__(
            path, get_lsloc(path, self.discoverer.languages)
        )
        self.assertEqual(0, proportion)
