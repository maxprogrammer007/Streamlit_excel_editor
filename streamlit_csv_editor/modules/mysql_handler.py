# modules/mysql_handler.py

import mysql.connector
import pandas as pd
from mysql.connector import Error


class MySQLHandler:
    def __init__(self, host, user, password, database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.conn
        except Error as e:
            raise ConnectionError(f"Failed to connect to MySQL: {e}")

    def close(self):
        if self.conn:
            self.conn.close()

    def list_databases(self):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute("SHOW DATABASES")
        return [db[0] for db in cursor.fetchall()]

    def list_tables(self, database):
        self.conn.database = database
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES")
        return [tbl[0] for tbl in cursor.fetchall()]

    def fetch_table(self, table_name):
        if self.conn is None or not self.conn.is_connected():
            self.connect()
        try:
            return pd.read_sql(f"SELECT * FROM `{table_name}`", self.conn)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch table '{table_name}': {e}")

    def write_dataframe(self, df, table_name, truncate=True):
        if self.conn is None or not self.conn.is_connected():
            self.connect()
        cursor = self.conn.cursor()

        try:
            if truncate:
                cursor.execute(f"TRUNCATE TABLE `{table_name}`")

            for _, row in df.iterrows():
                placeholders = ','.join(['%s'] * len(row))
                query = f"INSERT INTO `{table_name}` VALUES ({placeholders})"
                cursor.execute(query, tuple(row))

            self.conn.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to write data to '{table_name}': {e}")

    def execute_query(self, query):
        if self.conn is None or not self.conn.is_connected():
            self.connect()
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(result, columns=columns)
        except Exception as e:
            raise RuntimeError(f"Query execution failed: {e}")
