import configparser
import json
import psycopg2

from .database_connection import DatabaseConnection


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

        PrimaryFillingManager._fill_genres_films(data)

    @staticmethod
    def _fill_genres_films(data):
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
    def fill_people_and_related_data(id_tmdb, data):
        cast_data = data['cast']

        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                
                #known_for_department
                known_departments = set([person['known_for_department'] for person in cast_data])
                for department in known_departments:
                    cursor.execute("""
                        INSERT INTO known_for_department (known_for_department)
                        VALUES (%s)
                        ON CONFLICT (known_for_department) DO NOTHING
                    """, (department,))
                
                # Getting the ID of all known departments from the database
                cursor.execute("SELECT id, known_for_department FROM known_for_department")
                department_map = {row[1]: row[0] for row in cursor.fetchall()}

                # Filling in the people and people_films tables
                for person in cast_data:
                    # Inserting data into the people table
                    cursor.execute("""
                        INSERT INTO people (id_tmdb, name, gender, profile_path_photo)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id_tmdb) DO NOTHING
                        RETURNING id
                    """, (
                        person['id'],
                        person['name'],
                        person['gender'],
                        person['profile_path']
                    ))

                    # Get the ID of the inserted record, if it was added for the first time
                    people_id = cursor.fetchone()
                    
                    # If the record already exists, we get its ID
                    if not people_id:
                        cursor.execute("""
                            SELECT id FROM people WHERE id_tmdb = %s
                        """, (person['id'],))
                        people_id = cursor.fetchone()[0]

                    film_id = PrimaryFillingManager.get_film_id_by_id_tmdb(id_tmdb)
                    # Inserting data into the people_films table
                    cursor.execute("""
                        INSERT INTO people_films (id_film, id_people, id_known_for_department)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (id_film, id_people, id_known_for_department) DO NOTHING
                    """, (
                        film_id,
                        people_id,
                        department_map[person['known_for_department']]
                    ))

                connection.commit()

    @staticmethod
    def fill_keywords(id_tmdb, data):
        keywords = data.get('keywords', [])
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                film_id = PrimaryFillingManager.get_film_id_by_id_tmdb(id_tmdb)
                for keyword in keywords:
                    cursor.execute("""
                        INSERT INTO keywords (id, keywords, id_film)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """, (
                        keyword['id'], 
                        keyword['name'],  
                        film_id           
                    ))
    
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