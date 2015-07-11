import json
import os
import unittest

import database


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        path = (
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
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

    def test_connect(self):
        # Act
        self.database.connect()

        # Assert
        self.assertTrue(self.database._connection.is_connected())

    def test_disconnect(self):
        # Act
        self.database.connect()
        self.database.disconnect()

        # Assert
        self.assertFalse(self.database._connection.is_connected())

    def test_getone(self):
        # Arrange
        query = 'SELECT count(*) FROM projects'

        # Act
        self.database.connect()
        actual = self.database.getone(query)

        # Assert
        self.assertLess(0, actual)

    def test_getmany(self):
        # Arrange
        query = 'SELECT id, name FROM projects WHERE id IN (1,2)'
        expected = [(1, 'ruote-kit'), (2, 'ruote-kit')]

        # Act
        self.database.connect()
        actual = self.database.getmany(query)

        # Assert
        self.assertCountEqual(expected, actual)

    def tearDown(self):
        if self.database:
            self.database.disconnect()
