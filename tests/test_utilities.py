import os
import unittest
import tempfile
import subprocess

from dateutil.relativedelta import relativedelta
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

    def test_clone(self):
        with tempfile.TemporaryDirectory() as directory:
            # Arrange
            owner = 'andymeneely'
            name = 'squib'
            date = '2015-03-31 19:24:28'

            repository_root = directory
            repository_home = os.path.join(repository_root, '10868464')
            os.mkdir(repository_home)
            expected = {
                'sha': '784a0dcb90e798859ab24b69d4b8c12c200ed85d',
                'repository_path': os.path.join(repository_home, 'squib')
                }

            # Act
            actual = dict()
            actual['repository_path'] = utilities.clone(
                owner, name, repository_home, date
            )

            # Assert
            self.assertTrue(len(os.listdir(directory)) > 0)
            process = subprocess.Popen(
                'git log -1 --pretty="format:%H"',
                cwd=actual['repository_path'], shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            (out, err) = [i.decode() for i in process.communicate()]
            actual['sha'] = out
            self.assertEqual(expected, actual)

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

    def test_parse_datetime_delta(self):
        # Arrange
        datetime_deltas = [
            '1y',
            '1y1m',
            '1y1m1d',
            '1y1m1d1H',
            '1y1m1d1H1M',
            '1y1m1d1H1M1S',
            '1m1d1H1M1S',
            '1d1H1M1S',
            '1H1M1S',
            '1M1S',
            '1S',
            'ymdHMS',
            '11y11m11d11H11M11S',
            ''
        ]
        rd = relativedelta  # Alias for improved readability
        expected = [
            rd(years=1, months=0, days=0, hours=0, minutes=0, seconds=0),
            rd(years=1, months=1, days=0, hours=0, minutes=0, seconds=0),
            rd(years=1, months=1, days=1, hours=0, minutes=0, seconds=0),
            rd(years=1, months=1, days=1, hours=1, minutes=0, seconds=0),
            rd(years=1, months=1, days=1, hours=1, minutes=1, seconds=0),
            rd(years=1, months=1, days=1, hours=1, minutes=1, seconds=1),
            rd(years=0, months=1, days=1, hours=1, minutes=1, seconds=1),
            rd(years=0, months=0, days=1, hours=1, minutes=1, seconds=1),
            rd(years=0, months=0, days=0, hours=1, minutes=1, seconds=1),
            rd(years=0, months=0, days=0, hours=0, minutes=1, seconds=1),
            rd(years=0, months=0, days=0, hours=0, minutes=0, seconds=1),
            rd(years=0, months=0, days=0, hours=0, minutes=0, seconds=0),
            rd(years=11, months=11, days=11, hours=11, minutes=11, seconds=11),
            rd(years=0, months=0, days=0, hours=0, minutes=0, seconds=0),
        ]

        # Act
        actual = list()
        for datetime_delta in datetime_deltas:
            actual.append(utilities.parse_datetime_delta(datetime_delta))

        # Assert
        self.assertCountEqual(expected, actual)

    def test_is_cloneable(self):
        # Arrange
        owner = 'FFmpeg'
        name = 'FFmpeg'
        expected = (True, None)

        # Act
        actual = utilities.is_cloneable(owner, name)

        # Assert
        self.assertEqual(expected, actual)

        # Arrange
        owner = 'FFmpeg'
        name = 'FFmpe'
        expected = (False, '{0}/{1} is no longer active.'.format(owner, name))

        # Act
        actual = utilities.is_cloneable(owner, name)

        # Assert
        self.assertEqual(expected, actual)

        # Arrange
        owner = 'njulevi'
        name = 'QInsight'
        expected = (
            False, '{0}/{1} may have been deactivated.'.format(owner, name)
        )

        # Act
        actual = utilities.is_cloneable(owner, name)

        # Assert
        self.assertEqual(expected, actual)

        # Arrange
        owner = 'chambejp'
        name = 'external'
        expected = (
            False, '{0}/{1} may have been deactivated.'.format(owner, name)
        )

        # Act
        actual = utilities.is_cloneable(owner, name)

        # Assert
        self.assertEqual(expected, actual)

    def test_get_files(self):
        # Arrange
        path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), os.pardir, 'attributes', 'license'
            )
        )
        expected = [os.path.join(path, 'main.py')]

        # Act
        actual = utilities.get_files(path, language='Python')

        # Assert
        self.assertCountEqual(expected, actual)
