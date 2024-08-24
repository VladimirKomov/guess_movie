from abc import ABC, abstractmethod
import sys
import os

# Добавляем путь к src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.database_film_manager import GetData
from src.database.primary_filling_manager import PrimaryFillingManager
from game.game_manager import Game

# Abstract hint class


class Hint(ABC):
    @abstractmethod
    def apply(self, game):
        pass


# The first clue before the game starts
class KeywordsHint(Hint):
    def apply(self, game,limit_words = None):
        data = GetData.get_keywords(game.film[0])
        keywords_list = [keyword[0] for keyword in data]
        if limit_words is not None:
                    keywords_list = keywords_list[:limit_words]
        keywords = ', '.join(keywords_list)            
        return_str = f"Keywords: {keywords}"
        return return_str


# This is a genre hint
class GenreHint(Hint):
    def apply(self, game,):
        data = GetData.get_genre(game.film[0])
        genres_list = [keyword[0] for keyword in data]
        genres = ', '.join(genres_list)    
        return_str = f"The genres: {genres}"

        return return_str


# This is a year hint
class YearHint(Hint):
    def apply(self, game):
        data = game.film[8]
        return_str = f"Year: {data}"
        return return_str


# This is one actor hint
class ActorHint(Hint):
    def apply(self, game):
        data = GetData.get_actors(game.film[0], 'Acting', 1)
        actor_list = [keyword[0] for keyword in data]
        actor = ', '.join(actor_list)   
        return_str = f"Actor: {actor}"

        return return_str


# This is all actor hint
class ActorsHint(Hint):
    def apply(self, game):
        data = GetData.get_actors(game.film[0],'Acting', 15)
        actors_list = [keyword[0] for keyword in data]
        actors = ', '.join(actors_list)   
        return_str = f"Actors: {actors}"
        return return_str


# This is a hint for the full description of the film
class DescriptionHint(Hint):
    def apply(self, game):
        data = game.film[6]
        return_str = f"Description: {data}"
        return return_str


class ImageHint(Hint):
    def apply(self, game):
        data = game.film[2]
        return_str = f"https://image.tmdb.org/t/p/original{data}"
        return return_str
