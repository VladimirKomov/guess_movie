import configparser
import psycopg2

# 1. initial filling of the database with data received via the API

class PrimaryFillingManager:

    @staticmethod
    def __make_connection() -> psycopg2.extensions.connection:
        config = configparser.ConfigParser()
        script_dir = os.path.dirname(__file__)
        if not config.read(script_dir + "/config_database.ini"):
            raise FileNotFoundError("Could not read the configuration file.")

        connection = psycopg2.connect(
            database=config['database']['database'],
            user=config['database']['user'],
            password=config['database']['password'],
            host=config['database']['host'],
            port=config['database']['port']         
        )
        return connection