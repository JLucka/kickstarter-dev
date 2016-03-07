import os

import MySQLdb

from backend.locals import DB, PROPERTIES


class SQLConnector:
    def __init__(self):
        if os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/'):
            self.db = MySQLdb.connect(unix_socket=PROPERTIES['socket'], db=PROPERTIES['db'], user=PROPERTIES['user'])
        else:
            self.db = MySQLdb.connect(host=DB['host'], user=DB['user'], passwd=DB['password'], db=DB['db'])
        self.cursor = self.db.cursor()
        self.table_name = ""

    def select_all(self):
        self.cursor.execute("SELECT * FROM %s", (self.table_name))
        return self.cursor.fetchall()

    def select_from(self, columns):
        self.cursor.execute("SELECT %s FROM %s", ((', '.join(columns)), self.table_name))
        return self.cursor.fetchall()

    def select_all_where(self, condition):
        self.cursor.execute("SELECT * FROM %s WHERE %s", (self.table_name, condition))
        return self.cursor.fetchall()

    def select_where(self, columns, condition):
        self.cursor.execute("SELECT %s FROM %s WHERE %s", ((', '.join(columns)), self.table_name, condition))
        return self.cursor.fetchall()

    def insert_into(self, keys_and_values):
        keys = (', '.join(keys_and_values.keys()))
        values = (', '.join(map(str, keys_and_values.values())))
        try:
            query = ("INSERT INTO %s(%s) VALUES (%s)", (self.table_name, keys, values))
            self.cursor.execute(query)
            self.db.commit()
            return True
        except MySQLdb.Error, e:
            print query
            print e
            self.db.rollback()
            return False
