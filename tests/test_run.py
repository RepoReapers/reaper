import json
import os
import tempfile
import unittest

from lib import utilities
from lib.attributes import Attributes
from lib.database import Database
from lib.run import Run


class RunTestCase(unittest.TestCase):
    def setUp(self):
        parentpath = (
            os.path.abspath(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    os.pardir
                )
            )
        )
        manifestpath = os.path.join(parentpath, 'manifest.json')

        configpath = os.path.join(parentpath, 'config.json')
        rawsettings = None
        with open(configpath, 'r') as file_:
            rawsettings = json.load(file_)
        self.database = Database(rawsettings['options']['datasource'])

        rawmanifest = None
        with open(manifestpath, 'r') as file_:
            rawmanifest = json.load(file_)
        self.attributes = Attributes(rawmanifest['attributes'], self.database)

        self.threshold = rawsettings['options']['threshold']
        self.processes = 2

    def test_init(self):
        with tempfile.TemporaryDirectory() as directory:
            try:
                # Act
                run = Run(
                    directory, self.attributes, self.database, self.threshold,
                    self.processes
                )

                # Assert
                self.assertIsNotNone(run.run_id)
            finally:
                self.database.post(
                    'DELETE FROM reaper_runs WHERE id = {0}'.format(run.run_id)
                )
                self.database.disconnect()

    def test_save(self):
        with tempfile.TemporaryDirectory() as directory:
            # Arrange
            rresults = {
                'architecture': 9.9, 'continuous_integration': True,
                'community': 9, 'documentation': 9.9, 'history': 9.9,
                'license': True, 'management': 9.9, 'unit_test': 9.9,
                'state': 'active'
            }
            run = Run(
                directory, self.attributes, self.database, self.threshold,
                self.processes
            )

            # Act
            run._save(10868464, 99.99, rresults)

            # Assert
            try:
                self.database.connect()
                actual = self.database.get(
                    '''
                        SELECT project_id, architecture,
                            continuous_integration, community, documentation,
                            history, license, management, unit_test, state,
                            score
                        FROM reaper_results WHERE run_id = {0}
                    '''.format(run.run_id)
                )
                self.assertEqual(10868464, actual[0])
                self.assertEqual(9.9, actual[1])
                self.assertEqual(True, actual[2])
                self.assertEqual(9, actual[3])
                self.assertEqual(9.9, actual[4])
                self.assertEqual(9.9, actual[5])
                self.assertEqual(True, actual[6])
                self.assertEqual(9.9, actual[7])
                self.assertEqual(9.9, actual[8])
                self.assertEqual('active', actual[9])
                self.assertEqual(99.989998, actual[10])
            finally:
                self.database.post(
                    'DELETE FROM reaper_runs WHERE id = {0}'.format(run.run_id)
                )
                self.database.disconnect()
