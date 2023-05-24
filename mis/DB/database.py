import pandas as pd
import cx_Oracle as ora
from .query import Query


class DatabaseMis:

    def __init__(self, user, password, dsn):
        self._user = user
        self._password = password
        self._dsn = dsn
        self._connection = self._connect()

    def _connect(self):
        return ora.connect(self._user,
                           self._password,
                           self._dsn)

    def select(self, query: Query):
        cursor = self._connection.cursor()
        cursor.execute(query.query, query.parameters)
        header = [row[0] for row in cursor.description]
        data = pd.DataFrame(cursor.fetchall(), columns=header)
        return data

    def select1(self, query: Query):
        cursor = self._connection.cursor()
        cursor.prepare(query.query)
        print(cursor.bindvars)
        #print(cursor.description)
        cursor.execute(query.query, query.parameters)
        print(cursor.bindvars)

        header = [row[0] for row in cursor.description]
        data = pd.DataFrame(cursor.fetchall(), columns=header)
        return data

    def close(self):
        self._connection.close()