from src.database.database_connection import DatabaseConnection
from src.database.database_manager import ChoosingFilm
from src.game.hits import KeywordsHint


class Game:
    # creating a game
    def __init__(self, user, points):
        self.user = user
        self.points = points
        # getting a random movie for the game
        self.film = ChoosingFilm.get_random_film() 

