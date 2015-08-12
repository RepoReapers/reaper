import json
import os
import unittest

from attributes.state import main
from lib import database, dateutil, utilities


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
        settings = None
        with open(path, 'r') as file_:
            settings = json.load(file_)['options']['datasource']

        self.database = database.Database(settings)

    def test_main(self):
        # Arrange
        project_id = 284
        options = {'threshold': '6m'}
        expected = (True, 'active')

        # Act
        try:
            self.database.connect()
            with self.database.cursor() as cursor:
                actual = main.run(project_id, '', cursor, **options)
        finally:
            self.database.disconnect()

        # Assert
        self.assertEqual(expected, actual)

        # Arrange
        project_id = 66
        options = {'threshold': '6m'}
        expected = (False, 'dormant')

        # Act
        try:
            self.database.connect()
            with self.database.cursor() as cursor:
                actual = main.run(project_id, '', cursor, **options)
        finally:
            self.database.disconnect()

        # Assert
        self.assertEqual(expected, actual)

        # Arrange
        project_id = 3235653
        options = {'threshold': '6m'}
        expected = (False, 'dormant')

        # Act
        try:
            self.database.connect()
            with self.database.cursor() as cursor:
                actual = main.run(project_id, '', cursor, **options)
        finally:
            self.database.disconnect()

        # Assert
        self.assertEqual(expected, actual)
