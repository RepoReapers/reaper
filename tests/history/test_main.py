import json
import os
import unittest

from attributes.history import main
from lib import database


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
        project_id = 10868464  # andymeneely/squib
        options = {
            'threshold': 1,
            'minimumDurationInMonths': 1
        }

        # Act
        try:
            self.database.connect()
            with self.database.cursor() as cursor:
                (result, value) = main.run(project_id, '', cursor, **options)
        finally:
            self.database.disconnect()

        # Assert
        self.assertTrue(result)
        self.assertLess(0, value)

        # Arrange
        project_id = 581  # torvalds/linux
        options = {
            'threshold': 1,
            'minimumDurationInMonths': 1
        }

        # Act
        try:
            self.database.connect()
            with self.database.cursor() as cursor:
                (result, value) = main.run(project_id, '', cursor, **options)
        finally:
            self.database.disconnect()

        # Assert
        self.assertTrue(result)
        self.assertLess(0, value)

        # Arrange
        project_id = 66  # libraM/django-request-signer
        options = {
            'threshold': 1,
            'minimumDurationInMonths': 1
        }

        # Act
        try:
            self.database.connect()
            with self.database.cursor() as cursor:
                (result, value) = main.run(project_id, '', cursor, **options)
        finally:
            self.database.disconnect()

        # Assert
        self.assertFalse(result)
        self.assertEqual(0, value)
