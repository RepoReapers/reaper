import os
import unittest

import utilities


class UtilitiesTestCase(unittest.TestCase):
    def test_get_loc(self):
        path = os.path.join(
            os.path.dirname(__file__),
            'assets/projekt'
        )

        # Test: Get SLOC of source at ./assets/projekt
        expected = {
            'C':  {'cloc': 4, 'sloc': 6},
            'C/C++ Header': {'cloc': 0, 'sloc': 4},
            'Javascript': {'cloc': 1, 'sloc': 13},
            'Python': {'cloc': 1, 'sloc': 2}
        }

        sloc = utilities.get_loc(path)

        self.assertEqual(len(expected), len(sloc))
        for (k, v) in sloc.items():
            for (_k, _v) in v.items():
                self.assertEqual(expected[k][_k], _v)

        # Test: Get SLOC of only the directory 'include' for source at
        # ./assets/projekt
        expected = {
            'C/C++ Header': {'cloc': 0, 'sloc': 4},
        }

        sloc = utilities.get_loc(path, only=['include'])

        self.assertEqual(len(expected), len(sloc))
        for (k, v) in sloc.items():
            for (_k, _v) in v.items():
                self.assertEqual(expected[k][_k], _v)

        # Test: Get SLOC of only the directories 'include' and 'utilities' for
        # source at./assets/projekt
        expected = {
            'C/C++ Header': {'cloc': 0, 'sloc': 4},
            'Javascript': {'cloc': 1, 'sloc': 10},
        }

        sloc = utilities.get_loc(path, only=['include', 'utilities'])

        self.assertEqual(len(expected), len(sloc))
        for (k, v) in sloc.items():
            for (_k, _v) in v.items():
                self.assertEqual(expected[k][_k], _v)

        # Test: Missing source directory
        self.assertRaises(Exception, utilities.get_loc, '/home/nocturnal')

        # Test: Path is not a directory
        self.assertRaises(Exception, utilities.get_loc, '/bin/bash')
