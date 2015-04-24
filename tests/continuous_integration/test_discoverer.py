import os
import unittest

from attributes.continuous_integration.discoverer import CiDiscoverer
from tests import REPOS_PATH


class CiDiscovererTestCase(unittest.TestCase):
    def setUp(self):
        self.ci_discoverer = CiDiscoverer()

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_discover(self):
        # Test: Mocking no services configured
        ci_discoverer_mock = CiDiscoverer()
        ci_discoverer_mock.services = None

        self.assertRaises(Exception, ci_discoverer_mock.discover, path='')

        # Test: Project with Travis CI
        self.assertTrue(self.ci_discoverer.discover(
            os.path.join(REPOS_PATH, 'squib')
        ))

        # Test: Project with AppVeyor
        self.assertTrue(self.ci_discoverer.discover(
            os.path.join(REPOS_PATH, 'grunt')
        ))

        # Test: Project with both Travis CI and AppVeyor
        self.assertTrue(self.ci_discoverer.discover(
            os.path.join(REPOS_PATH, 'grunt')
        ))

        # Test: Project with no CI (when these tests were written)
        self.assertFalse(self.ci_discoverer.discover(
            os.path.join(REPOS_PATH, 'django')
        ))

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_travis(self):
        # Test: Project with Travis CI
        self.assertTrue(self.ci_discoverer.__travis__(
            os.path.join(REPOS_PATH, 'squib')
        ))

        # Test: Project with no Travis CI
        self.assertFalse(self.ci_discoverer.__travis__(
            os.path.join(REPOS_PATH, 'django')
        ))

    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_appveyor(self):
        # Test: Project with AppVeyor CI
        self.assertTrue(self.ci_discoverer.__appveyor__(
            os.path.join(REPOS_PATH, 'grunt')
        ))

        # Test: Project with no AppVeyor CI
        self.assertFalse(self.ci_discoverer.__appveyor__(
            os.path.join(REPOS_PATH, 'squib')
        ))
