import contextlib
import sys

import mysql.connector


class DatabaseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Database(object):
    def __init__(self, settings):
        self.settings = settings
        self.settings['autocommit'] = True
        self._connection = None

    def connect(self):
        try:
            self._connection = mysql.connector.connect(**self.settings)
            self._connection.connect()
        except mysql.connector.Error as e:
            message = (
                'Unable to establish database connection. Error: {0}'
            ).format(str(e))
            raise DatabaseError(message)

    def disconnect(self):
        try:
            if self._connection and self._connection.is_connected():
                self._connection.disconnect()
        except mysql.connector.Error as e:
            message = (
                'Unable to disconnect from database. Error: {0}'
            ).format(str(e))
            raise DatabaseError(message)

    def getone(self, query):
        return self._get(query, count=1)

    def getmany(self, query):
        return self._get(query)

    def execute(self, query):
        if self._connection:
            try:
                with self._get_cursor() as cursor:
                    cursor.execute(query)
            except mysql.connector.Error as e:
                message = (
                    'Failed executing query {0}. Error: {1}'
                ).format(sql, str(e))
                raise DatabaseError(message)
            finally:
                if cursor:
                    cursor.close()
        else:
            raise DatabaseError('Not connnected to the database.')

    @contextlib.contextmanager
    def _get_cursor(self):
        cursor = self._connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def _get(self, query, count=None):
        if self._connection:
            try:
                rows = list()
                with self._get_cursor() as cursor:
                    cursor.execute(query)
                    for row in cursor.fetchall():
                        rows.append(row)

                if count is None:
                    return rows
                else:
                    if len(rows) >= 1 and len(rows[0]) >= 1:
                        return rows[0][0]
            except mysql.connector.Error as e:
                message = (
                    'Failed executing query {0}. Error: {1}'
                ).format(query, str(e))
                raise DatabaseError(message)
        else:
            raise DatabaseError('Not connnected to the database.')
