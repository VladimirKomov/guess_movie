from src.database.database_connection import DatabaseConnection

class GetData:
    # getting a random movie for the game
    @staticmethod
    def get_random_film():
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM films ORDER BY RANDOM() LIMIT 1")
                film = cursor.fetchone()
                return film

    # Retrieves keywords associated with a specific film from the database
    @staticmethod
    def get_keywords(id_film):
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                 # Select keywords where the film ID matches
                cursor.execute("SELECT keywords FROM keywords WHERE id_film = %s", (id_film,))
                keywords = cursor.fetchall()
                return keywords


    # Retrieves genres associated with a specific film from the database
    @staticmethod
    def get_genre(id_film):
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                # Select genres where the film ID matches
                cursor.execute('''SELECT genres.name FROM genres
                                  JOIN genres_films ON genres.id = genres_films.id_genre
                                  WHERE genres_films.id_film = %s''', (id_film,))
                genres = cursor.fetchall()
                return genres
            
    # Retrieves actors related to a specific film and department, with a limit on the number of results
    @staticmethod
    def get_actors(id_film, department_id, limit):
        with DatabaseConnection() as connection:
            with connection.cursor() as cursor:
                # Select the names of people who are related to the film and the specific department (acting)
                cursor.execute('''SELECT people.name FROM people
                        JOIN people_films ON people.id = people_films.id_people
                        WHERE people_films.id_film = %s
                        AND people_films.id_known_for_department = %s
                        LIMIT %s''', (id_film, department_id, limit))
                people = cursor.fetchall()
                return people
            

              