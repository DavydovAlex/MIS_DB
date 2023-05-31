import abc

import oracledb as ora
#rom query import Query
import pandas as pd
from abc import ABC


class Query(ABC):
    statement = None
    params = None

    def __init__(self, statement, params={}):
        self.statement = statement
        self.params = params


class MultyQuery(Query):
    pass


class SingleQuery(Query):
    pass


class Cursor(ABC):
    header = None
    params = None
    description = None
    _iter_object = None

    def __init__(self, iter_object):
        self._iter_object = iter_object


class OracleCursor(Cursor):
    def __init__(self, iter_object: ora.Cursor):
        super().__init__(iter_object)
        self.header = [row[0] for row in iter_object.description]
        print(self.header)
        self.description = iter_object.description

    def __iter__(self):
        return self

    def __next__(self):
        return self._iter_object.__next__()


class Database(ABC):
    user = None
    password = None
    dsn = None

    def __init__(self, user, password, dsn):
        self.user = user
        self.password = password
        self.dsn = dsn

    @abc.abstractmethod
    def execute(self, query: Query):
        pass

    @abc.abstractmethod
    def open_connection(self):
        pass

    @abc.abstractmethod
    def close_connection(self):
        pass


class Oracle(Database):

    def __init__(self, user, password, dsn):
        super().__init__(user, password, dsn)
        ora.init_oracle_client() #TODO вынести в отдельный метод ?
        self.connection = self.open_connection()

    def open_connection(self):
        return ora.connect(user=self.user,
                           password=self.password,
                           dsn=self.dsn)

    def close_connection(self):
        self.connection.close()

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query.statement, query.params)
        return OracleCursor(cursor)

class Database:

    def __init__(self, user, password, dsn):
        ora.init_oracle_client()
        self._user = user
        self._password = password
        self._dsn = dsn
        self._connection = self._connect()


    def _connect(self):
        return ora.connect(user=self._user,
                           password=self._password,
                           dsn=self._dsn)

    def execute(self, query:Query):
        cursor = self._connection.cursor()


    def select(self, query: Query):
        cursor = self._connection.cursor()
        print(type(cursor))
        cursor.prepare(query.query)
        names = cursor.bindnames()
        print(names)
        cursor.execute(None, query.parameters)
        print(cursor.description)
        header = [row[0] for row in cursor.description]
        data = pd.DataFrame(cursor.fetchall(), columns=header)
        print(data)
        #return data

    def close(self):
        self._connection.close()


if __name__ == '__main__':
    dsn = """
            (DESCRIPTION =
            (ADDRESS_LIST =
              (ADDRESS = (PROTOCOL = TCP)(HOST = 10.101.39.53)(PORT = 1521))
            )
            (CONNECT_DATA =
              (SERVICE_NAME = nsocluster)
        	  (SERVER = DEDICATED)
            )
          )
            """
    db = Oracle('YUVTOKAREVA_DB', 'p123', dsn)
    query = Query('Select * from D_AGENTS where rownum<=10')
    cursor = db.execute(query)