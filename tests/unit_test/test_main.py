import os
import unittest

from attributes.unit_test import main
from tests import REPOS_PATH


class MainTestCase(unittest.TestCase):
    @unittest.skip('TODO')
    def test_main(self):
        # Test: Project using Mocha
        self.assertTrue(main.run(
            0, os.path.join(REPOS_PATH, 'superagent'), None
        ))

        # Test: Project with no unit tests (when these tests were written)
        self.assertFalse(main.run(
            0, os.path.join(REPOS_PATH, 'javascript'), None
        ))
