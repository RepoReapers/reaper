import os
import unittest
import tempfile

from lib import utilities
from tests import ASSETS_PATH


class UtilitiesTestCase(unittest.TestCase):
    def test_get_loc(self):
        path = os.path.join(ASSETS_PATH, 'projekt')

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
        #   ./assets/projekt
        expected = {
            'C/C++ Header': {'cloc': 0, 'sloc': 4},
        }

        sloc = utilities.get_loc(path, files=['include/projekt.h'])

        self.assertEqual(len(expected), len(sloc))
        for (k, v) in sloc.items():
            for (_k, _v) in v.items():
                self.assertEqual(expected[k][_k], _v)

        # Test: Get SLOC of only the directories 'include' and 'utilities' for
        #   source at ./assets/projekt
        expected = {
            'C/C++ Header': {'cloc': 0, 'sloc': 4},
            'Javascript': {'cloc': 1, 'sloc': 10},
        }

        sloc = utilities.get_loc(
            path, files=['include/projekt.h', 'utilities/projekt.js']
        )

        self.assertEqual(len(expected), len(sloc))
        for (k, v) in sloc.items():
            for (_k, _v) in v.items():
                self.assertEqual(expected[k][_k], _v)

        # Test: Missing source directory
        self.assertRaises(Exception, utilities.get_loc, '/home/nocturnal')

        # Test: Path is not a directory
        self.assertRaises(Exception, utilities.get_loc, '/bin/bash')

    def test_search(self):
        path = os.path.join(
            os.path.dirname(__file__),
            'assets/projekt'
        )

        # Test: Search for '#include <stdio.h>' in source at ./assets/projekt
        expected = ['projekt.c']
        self.assertListEqual(
            expected,
            utilities.search('#include <stdio.h>', path)
        )

        # Test: Search for '#include <stdio.h>' in '*.c' files in source at
        #   ./assets/projekt
        expected = ['projekt.c']
        self.assertListEqual(
            expected,
            utilities.search(
                '#include <stdio.h>', path, include=['*.c']
            )
        )

        # Test: Search for '#include <stdio.h>' in '*.c' and '*.js' files in
        #   source at ./assets/projekt
        expected = ['projekt.c']
        self.assertListEqual(
            expected,
            utilities.search(
                '#include <stdio.h>', path, include=['*.c', '*.js']
            )
        )

        # Test: Search for '#include <stdio.h>' in '*.h' files in source at
        #   ./assets/projekt
        self.assertIsNone(
            utilities.search(
                '#include <stdio.h>', path, include=['*.h']
            )
        )

        # Test: Missing source directory
        self.assertRaises(
            Exception, utilities.search,
            pattern='#include <stdio.h>', path='/home/nocturnal',
        )

        # Test: Path is not a directory
        self.assertRaises(
            Exception, utilities.search,
            pattern='#include <stdio.h>', path='/bin/bash',
        )

    def test_download(self):
        with tempfile.TemporaryDirectory() as directory:
            # Arrange
            url = 'https://api.github.com/repos/ffmpeg/ffmpeg/tarball'
            expected = os.path.join(directory, 'FFmpeg-FFmpeg-')

            # Act
            actual = utilities.download(url, directory)

            # Assert
            self.assertTrue(len(os.listdir(directory)) > 0)
            self.assertTrue(expected in actual)

    def test_read(self):
        # Arrange
        path = os.path.join(ASSETS_PATH, 'test.json')
        expected = {'message': 'hello world!!!'}

        # Act
        actual = utilities.read(open(path))

        # Assert
        self.assertEqual(expected, actual)

    def test_read_error(self):
        # Arrange
        path = os.path.join(ASSETS_PATH, 'test.txt')

        # Assert
        self.assertRaises(Exception, utilities.read, open(path))
