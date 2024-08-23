from abc import ABC, abstractmethod

from src.database.database_manager import GetData
from src.database.primary_filling_manager import PrimaryFillingManager
# Abstract hint class

class Hint(ABC):
    @abstractmethod
    def apply(self, game):
        pass


# The first clue before the game starts !!!! Нужно указать корректный метод
class KeywordsHint(Hint):
    def apply(self, game):
        data = GetData.get_keywords(game.film[0])
        return_str = f"Your first clue! Keywords that describe the film: {data}"
        return return_str
        

# This is a genre hint !!!! Нужно указать корректный метод
class GenreHint(Hint):
    def apply(self, game):
        data = GetData.get_genre(game.film['id'])
        return_str = f"Here is the genres of the film: {data}"
        return return_str
    

# This is a year hint !!!! Нужно указать корректный метод
class YearHint(Hint):
    def apply(self, game):
        data = game.film['release_date']
        return_str = f"Here is the year of the film: {data}"
        return return_str
    
# This is one actor hint !!!!Нужно указать корректный метод
class ActorHint(Hint):
    def apply(self, game):
        data = PrimaryFillingManager.get_actor(game.film['id'], 15,1)
        return_str = f"Here is one actor of the film: {data}"
        return return_str     


# This is all actor hint !!!!Нужно указать корректный метод
class ActorsHint(Hint):
    def apply(self, game):
        data = PrimaryFillingManager.get_actors(game.film['id'], 15, 1000)
        return_str = f"Here is all actors of the film: {data}"
        return return_str
    

# This is a hint for the full description of the film  !!!!Нужно указать корректный метод  
class DescriptionHint(Hint):
    def apply(self, game):
        data = game.film['overview']
        return_str = f"Here is the description of the film: {data}"
        return return_str