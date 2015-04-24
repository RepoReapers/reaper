import os
import unittest

from attributes.continuous_integration import main
from tests import REPOS_PATH


class MainTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_main(self):
        # Test: Project with Travis CI
        self.assertTrue(main.run(
            -1, os.path.join(REPOS_PATH, 'squib'), None
        ))

        # Test: Project with AppVeyor
        self.assertTrue(main.run(
            -1, os.path.join(REPOS_PATH, 'grunt'), None
        ))

        # Test: Project with both Travis CI and AppVeyor
        self.assertTrue(main.run(
            -1, os.path.join(REPOS_PATH, 'grunt'), None
        ))

        # Test: Project with no CI (when these tests were written)
        self.assertFalse(main.run(
            -1, os.path.join(REPOS_PATH, 'django'), None
        ))
