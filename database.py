import sqlite3
from sqlite3 import Error


class Database:

    def __init__(self, db_file_path='test.db'):
        self.db_file_path = db_file_path

    def get_connection(self):
        return sqlite3.connect(self.db_file_path)

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS TRACE")
        sql = '''CREATE TABLE TRACE (ID VARCHAR(256), HOP INT, IP VARCHAR(256), PRIMARY KEY (ID, HOP))'''
        cursor.execute(sql)
        conn.commit()
        conn.close()


if "__main__" == __name__:
    Database().create_tables()
