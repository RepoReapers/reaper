import contextlib
import sys

import mysql.connector as mysql


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
            self._connection = mysql.connect(**self.settings)
        except mysql.Error as e:
            msg = 'Failure in connecting to database. Error: {0}'.format(e)
            raise DatabaseError(msg)

    def disconnect(self):
        try:
            if self._connection:
                self._connection.disconnect()
            self._connection = None
        except mysql.Error as e:
            msg = 'Failure in disconnecting from database. Error: {0}'.format(
                e
            )
            raise DatabaseError(msg)

    def get(self, query):
        try:
            rows = None
            with self.cursor() as cursor:
                cursor.execute(query)
                _rows = cursor.fetchall()
                if _rows:
                    rows = list()
                    for row in _rows:
                        rows.append(row)
                    if len(rows) == 1:
                        rows = rows[0]
                        if len(rows) == 1:
                            rows = rows[0]

            return rows
        except mysql.Error as e:
            msg = 'Failure in executing query {0}. Error: {1}'.format(query, e)
            raise DatabaseError(msg)

    def post(self, query, data=None):
        try:
            with self.cursor() as cursor:
                cursor.execute(query, params=data)

                if cursor.lastrowid is not None:
                    return cursor.lastrowid
                return cursor.rowcount
        except mysql.Error as e:
            msg = 'Failure in executing query {0}. Error: {1}'.format(query, e)
            raise DatabaseError(msg)

    @contextlib.contextmanager
    def cursor(self):
        if not self._connected:
            msg = 'An active database connection is needed to create a cursor.'
            raise DatabaseError(msg)

        cursor = self._connection.cursor()
        try:
            yield cursor
        except:
            raise
        finally:
            cursor.close()

    @property
    def _connected(self):
        connected = False
        if self._connection is not None and self._connection.is_connected():
            connected = True
        return connected

    def __getstate__(self):
        state = self.__dict__.copy()
        if isinstance(self._connection, mysql.connection.MySQLConnection):
            self.disconnect()
            state['_connection'] = ''
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        if isinstance(self._connection, str):
            self.connect()
