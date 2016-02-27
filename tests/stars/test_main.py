import json
import os
import unittest

from attributes.stars import main
from lib import core, database, dateutil, utilities


class MainTestCase(unittest.TestCase):
    def setUp(self):
        path = (
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        os.pardir,
                        os.pardir
                    )
                ),
                'config.json'
            )
        )
        config = None
        with open(path, 'r') as file_:
            config = utilities.read(file_)

        self.database = database.Database(config['options']['datasource'])
        core.config = config
        utilities.TOKENIZER = core.Tokenizer()

    def test_main(self):
        # Arrange
        project_id = 24397
        options = {'threshold': 0}
        expected = (True, 3660)

        # Act
        try:
            self.database.connect()
            with self.database.cursor() as cursor:
                actual = main.run(project_id, '', cursor, **options)
        finally:
            self.database.disconnect()

        # Assert
        self.assertLessEqual(expected, actual)

        # Arrange
        project_id = 9043022
        options = {'threshold': 0}
        expected = (True, 0)

        # Act
        try:
            self.database.connect()
            with self.database.cursor() as cursor:
                actual = main.run(project_id, '', cursor, **options)
        finally:
            self.database.disconnect()

        # Assert
        self.assertLessEqual(expected, actual)

        # Arrange
        project_id = 13480378
        options = {'threshold': 0}
        expected = (False, None)

        # Act
        try:
            self.database.connect()
            with self.database.cursor() as cursor:
                actual = main.run(project_id, '', cursor, **options)
        finally:
            self.database.disconnect()

        # Assert
        self.assertEqual(expected, actual)
