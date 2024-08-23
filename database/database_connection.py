import os
import psycopg2
import configparser
from psycopg2 import extensions

class DatabaseConnection:
    def __init__(self, config_path="config_database.ini"):
        self.__config_path = config_path
        self.__connection = self.__make_connection()

    @property
    def connection(self):
        return self.__connection

    def __make_connection(self) -> extensions.connection:
        config = configparser.ConfigParser()
        script_dir = os.path.dirname(__file__)
        if not config.read(os.path.join(script_dir, self.__config_path)):
            raise FileNotFoundError("Could not read the configuration file.")

        connection = psycopg2.connect(
            database=config['database']['database'],
            user=config['database']['user'],
            password=config['database']['password'],
            host=config['database']['host'],
            port=config['database']['port']
        )
        return connection

    def close_connection(self):
        if self.__connection:
            self.__connection.close()
            self.__connection = None

    def __enter__(self):
        return self.__connection

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()
