import sqlite3


class Database:
    def __init__(self, db_file_path="traces.sqlite"):
        self.db_file_path = db_file_path

    def get_connection(self):
        return sqlite3.connect(self.db_file_path)

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS TRACE")
        sql = """CREATE TABLE TRACE (ID VARCHAR(256), HOP INT, IP VARCHAR(256),
        COUNTRY VARCHAR(256), CITY VARCHAR(256), ISP VARCHAR(256),
        LATITUDE FLOAT, LONGITUDE FLOAT,DATE_CREATED DATETIME, PRIMARY KEY (ID, HOP))"""
        cursor.execute(sql)
        conn.commit()
        conn.close()
        print("table TRACE created!!")


if "__main__" == __name__:
    Database().create_tables()
