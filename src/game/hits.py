from abc import ABC, abstractmethod

from src.database.database_manager import GetData
from src.database.primary_filling_manager import PrimaryFillingManager

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
        return_str = f"Your first clue! Keywords that describe the film: {keywords}"
        return return_str


# This is a genre hint
class GenreHint(Hint):
    def apply(self, game,):
        data = GetData.get_genre(game.film[0])
        genres_list = [keyword[0] for keyword in data]
        genres = ', '.join(genres_list)    
        return_str = f"Here is the genres of the film: {genres}"
        return return_str


# This is a year hint
class YearHint(Hint):
    def apply(self, game):
        data = game.film[8]
        return_str = f"Here is the year of the film: {data}"
        return return_str


# This is one actor hint
class ActorHint(Hint):
    def apply(self, game):
        data = GetData.get_actors(game.film[0], 2, 1)
        actor_list = [keyword[0] for keyword in data]
        actor = ', '.join(actor_list)   
        return_str = f"Here is one actor of the film: {actor}"
        return return_str


# This is all actor hint
class ActorsHint(Hint):
    def apply(self, game):
        data = GetData.get_actors(game.film[0], 2, 15)
        actors_list = [keyword[0] for keyword in data]
        actors = ', '.join(actors_list)   
        return_str = f"Here is all actors of the film: {actors}"
        return return_str


# This is a hint for the full description of the film
class DescriptionHint(Hint):
    def apply(self, game):
        data = game.film[6]
        return_str = f"Here is the description of the film: {data}"
        return return_str
