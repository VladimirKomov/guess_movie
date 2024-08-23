from src.database.database_connection import DatabaseConnection


class ChoosingFilm:
    # getting a random movie for the game
    @staticmethod
    def get_random_movie():
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM movies ORDER BY RANDOM() LIMIT 1")
                film = cursor.fetchone()
                return film

class GetData:
    # Retrieves keywords associated with a specific film from the database
    @staticmethod
    def get_keywords(id_film):
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                 # Select keywords where the film ID matches
                cursor.execute("SELECT keywords FROM keywords WHERE id_film = %s", (id_film))
                keywords = cursor.fetchone()
                return keywords


    # Retrieves genres associated with a specific film from the database
    @staticmethod
    def get_genre(id_film):
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                # Select genres where the film ID matches
                cursor.execute("SELECT genres FROM guessed_films WHERE id_film = %s", (id_film))
                genres = cursor.fetchone()
                return genres
            
    # Retrieves actors related to a specific film and department, with a limit on the number of results
    @staticmethod
    def get_actors(id_film, department_id, limit):
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                # Select the names of people who are related to the film and the specific department (acting)
                cursor.execute(''' SELECT people.name FROM people
                        JOIN people_films ON people.id = people_films.id_people
                        JOIN people_known_for ON people.id = people_known_for.id_people
                        WHERE people_films.id_film = %s
                        AND people_known_for.id_known_for_department = %s
                        LIMIT %s''', (id_film, department_id, limit))
                people = cursor.fetchall()
                return people
            

              