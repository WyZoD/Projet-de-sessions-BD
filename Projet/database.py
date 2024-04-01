import pymysql
from flask.cli import load_dotenv
import os

from werkzeug.security import generate_password_hash

load_dotenv()


def get_db_connection():
    return pymysql.connect(
        host=os.environ.get("host"),
        port=int(os.environ.get("port")),
        user=os.environ.get("user"),
        password=os.environ.get("password"),
        db=os.environ.get("database"),
        autocommit=True
    )


def add_user(username, password, email, name, address):
    hashed_password = generate_password_hash(password)
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("Insert into users (username, password, email, name, address, InscriptionDate) "
                               "values (%s, %s, %s, %s, %s, NOW())",
                               (username, hashed_password, email, name, address,))
                connection.commit()
                return True
            except Exception as e:
                print(e)
                connection.rollback()
                return False


