import sqlite3 as sql


class SQLQuery:
    def __init__(self, database_file: str):
        self.database_file = database_file
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sql.connect(self.database_file)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
