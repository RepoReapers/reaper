import os
import unittest

import utilities


class UtilitiesTestCase(unittest.TestCase):
    def test_get_sloc(self):
        path = os.path.join(
            os.path.dirname(__file__),
            'assets/projekt'
        )

        # Test: Get SLOC of source at ./assets/projekt
        expected = {'C': 6, 'C/C++ Header': 4, 'Javascript': 3, 'Python': 2}

        sloc = utilities.get_sloc(path)

        self.assertEqual(len(expected), len(sloc))
        for (k, v) in sloc.items():
            self.assertEqual(expected[k], v)

        # Test: Get SLOC of only include for source at ./assets/projekt
        expected = {'C/C++ Header': 4}

        sloc = utilities.get_sloc(path, only='include')

        self.assertEqual(len(expected), len(sloc))
        for (k, v) in sloc.items():
            self.assertEqual(expected[k], v)

        # Test: Missing source directory
        self.assertRaises(Exception, utilities.get_sloc, '/home/nocturnal')

        # Test: Path is not a directory
        self.assertRaises(Exception, utilities.get_sloc, '/bin/bash')
