import configparser
import json
import psycopg2

from database_connection import DatabaseConnection


# 1. initial filling of the database with data received via the API

class PrimaryFillingManager:

    # load from json file
    @staticmethod
    def read_json(json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data

    # first genres
    @staticmethod
    def fill_genres(data):
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                for genre in data['genres']:
                    cursor.execute("""
                        INSERT INTO genres (
                            id_tmdb, name
                        ) VALUES (%s, %s)
                        ON CONFLICT (id_tmdb) DO NOTHING
                    """, (
                        genre['id'],
                        genre['name']
                    ))
                connection.commit()

    # second movies
    @staticmethod
    def fill_movies(data):
        # Connecting to the database and inserting data
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                for movie in data['results']:
                    cursor.execute("""
                        INSERT INTO films (
                            adult, backdrop_path, id_tmdb, original_language, title, overview, 
                            poster_path, release_date, vote_average
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id_tmdb) DO NOTHING
                    """, (
                        movie['adult'],
                        movie['backdrop_path'],
                        movie['id'],
                        movie['original_language'],
                        movie['title'],
                        movie['overview'],
                        movie['poster_path'],
                        movie['release_date'],
                        movie['vote_average']
                    ))
                # confirm changes
                connection.commit()

    @staticmethod
    def fill_genres_films(data):
        # filling in the connection between films and genres
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                for movie in data['results']:
                    for genre_id in movie['genre_ids']:
                        genre_id = PrimaryFillingManager.get_genre_id_by_id_tmdb(genre_id)
                        movie_id = PrimaryFillingManager.get_film_id_by_id_tmdb(movie['id'])
                        cursor.execute("""
                            INSERT INTO genres_films (id_film, id_genre) VALUES (%s, %s)
                            ON CONFLICT (id_film, id_genre) DO NOTHING
                        """, (movie_id, genre_id))
                connection.commit()

    @staticmethod
    def get_genre_id_by_id_tmdb(id_tmdb: int):
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM genres WHERE id_tmdb = %s", (id_tmdb,))
                return cursor.fetchone()
            
    @staticmethod
    def get_film_id_by_id_tmdb(id_tmdb: int):
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM films WHERE id_tmdb = %s", (id_tmdb,))
                return cursor.fetchone()

    @staticmethod
    def get_all_movies():
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM films")
                return cursor.fetchall()