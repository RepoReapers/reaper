import os
import unittest

from attributes.continuous_integration import main
from tests import REPOS_PATH


class MainTestCase(unittest.TestCase):
    @unittest.skipIf(not os.path.exists(REPOS_PATH), 'setup.sh not run.')
    def test_main(self):
        # Test: Project with Travis CI
        (result, value) = main.run(
            -1, os.path.join(REPOS_PATH, 'squib'), None
        )
        self.assertTrue(result)
        self.assertTrue(value)

        # Test: Project with AppVeyor
        (result, value) = main.run(
            -1, os.path.join(REPOS_PATH, 'grunt'), None
        )
        self.assertTrue(result)
        self.assertTrue(value)

        # Test: Project with both Travis CI and AppVeyor
        (result, value) = main.run(
            -1, os.path.join(REPOS_PATH, 'grunt'), None
        )
        self.assertTrue(result)
        self.assertTrue(value)

        # Test: Project with no CI (when these tests were written)
        (result, value) = main.run(
            -1, os.path.join(REPOS_PATH, 'django'), None
        )
        self.assertFalse(result)
        self.assertFalse(value)
