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
        print self.table_name
        try:
            self.cursor.execute("SELECT * FROM %s" % (self.table_name,))
        except MySQLdb, e:
            print e
        return self.cursor.fetchall()

    def select_from(self, columns):
        query = "SELECT %s" + " FROM %s" % self.table_name
        self.cursor.execute(query, ((', '.join(columns)), ))
        return self.cursor.fetchall()

    def select_all_where(self, condition):
        query = "SELECT * FROM %s" % "self.table_name" + " WHERE %s"
        self.cursor.execute(query, (condition,))
        return self.cursor.fetchall()

    def select_where(self, columns, condition):
        query = "SELECT %s " + "FROM %s " % self.table_name +" WHERE %s"
        self.cursor.execute(query, ((', '.join(columns)), condition))
        return self.cursor.fetchall()

    def insert_into(self, keys_and_values):
        keys = (', '.join(keys_and_values.keys()))
        values = (', '.join(map(str, keys_and_values.values())))
        try:
            query = ("INSERT INTO %s" % self.table_name + "(%s) VALUES (%s)")
            self.cursor.execute(query, (keys, values))
            self.db.commit()
            return True
        except MySQLdb.Error, e:
            print query
            print e
            self.db.rollback()
            return False
