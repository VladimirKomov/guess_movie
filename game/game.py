from src.database.database_connection import DatabaseConnection
from src.database.database_manager import ChoosingFilm


class Game:
    # creating a game
    def __init__(self, user, points, film):
        self.user = user
        self.points = points
        # getting a random movie for the game
        self.film = ChoosingFilm._get_random_movie() 
