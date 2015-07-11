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

    def test_get_empty(self):
        # Arrange
        query = 'SELECT id, name FROM projects WHERE id = 111111111'
        expected = []

        # Act
        self.database.connect()
        actual = self.database.get(query)

        # Assert
        self.assertCountEqual(expected, actual)

    def test_get_single(self):
        # Arrange
        query = 'SELECT id, name FROM projects WHERE id = 1'
        expected = [(1, 'ruote-kit')]

        # Act
        self.database.connect()
        actual = self.database.get(query)

        # Assert
        self.assertCountEqual(expected, actual)

    def test_get_multiple(self):
        # Arrange
        query = 'SELECT id, name FROM projects WHERE id IN (1,2)'
        expected = [(1, 'ruote-kit'), (2, 'ruote-kit')]

        # Act
        self.database.connect()
        actual = self.database.get(query)

        # Assert
        self.assertCountEqual(expected, actual)

    def test_post(self):
        # Arrange
        tname = 'foo'
        query = 'CREATE TABLE {0} (bar INT)'.format(tname)
        expected = [(tname,)]

        # Act
        self.database.connect()
        self.database.post(query)
        actual = self.database.get('SHOW TABLES LIKE \'{0}\''.format(tname))

        # Assert
        try:
            self.assertCountEqual(expected, actual)
        finally:
            with self.database.cursor() as cursor:
                cursor.execute('DROP TABLE IF EXISTS {0}'.format(tname))

    def tearDown(self):
        if self.database:
            self.database.disconnect()
