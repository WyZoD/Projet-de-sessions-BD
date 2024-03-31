import os

import pymysql
from flask.cli import load_dotenv


class Database:
    def __init__(self):
        load_dotenv()
        self.host = os.environ.get("host")
        self.port = int(os.environ.get("port"))
        self.database = os.environ.get("database")
        self.user = os.environ.get("user")
        self.password = os.environ.get("password")
        self._open_sql_connection()



    def _open_sql_connection(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
            autocommit=True
        )

        self.cursor = self.connection.cursor()