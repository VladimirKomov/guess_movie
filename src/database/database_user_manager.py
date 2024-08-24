import psycopg2
from psycopg2 import sql
from werkzeug.security import generate_password_hash, check_password_hash

from src.database.database_connection import DatabaseConnection




class UserDataBaseManager:
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def register_user(self, nick, email, name, birthdate, password):
        # Registering a new user
        hashed_password = generate_password_hash(password)

        with self.db_connection.connection.cursor() as cursor:
            try:
                cursor.execute("""
                    INSERT INTO users (nick, e_mail, name, birthdate, password)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nick, email, name, birthdate, hashed_password))
                self.db_connection.connection.commit()
                return True
            except psycopg2.IntegrityError:
                self.db_connection.connection.rollback()
                return False

    def authenticate_user(self, nick_or_email, password):
        # User authorization
        with self.db_connection.connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM users WHERE nick = %s OR e_mail = %s
            """, (nick_or_email, nick_or_email))
            user = cursor.fetchone()

            if user and check_password_hash(user[6], password):  # user[6] - это поле password
                return user
            return None

    def user_exists(self, nick, email):
        # Verification of the user's existence
        with self.db_connection.connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM users WHERE nick = %s OR e_mail = %s
            """, (nick, email))
            return cursor.fetchone() is not None
