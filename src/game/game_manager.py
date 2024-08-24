from database_game_manager import InsertGameData
from src.database.database_film_manager import GetData
from src.game.hits import *
from rapidfuzz import fuzz

class Game:
    # creating a game
    def __init__(self, user):
        self.user = user
        # getting a random movie for the game
        self.film = GetData.get_random_film()

    # 1. getting a keyword hint in the current game
    # the string will be returned
    def get_keywordsHint(self):
        keywords_hint = KeywordsHint()
        keywords_result = keywords_hint.apply(self, 5)
        return keywords_result

    # 2.  getting hints on genres in the current game
    # the string will be returned
    def get_genreHint(self):
        genre_hint = GenreHint()
        genre_hint.apply(self)
        genres_result = genre_hint.apply(self)
        return genres_result

    # 3. getting hints on actors in the current game
    # the string will be returned
    def get_actorsHint(self):
        actor_hint = ActorsHint()
        actors_result = actor_hint.apply(self)
        return actors_result

    # 4. getting hints on year in the current game
    # the string will be returned
    def get_yearHint(self):
        year_hint = YearHint()
        year_result = year_hint.apply(self)
        return year_result

    # 5. getting hints on description in the current game
    # the string will be returned
    def get_descriptionHint(self):
        description_hint = DescriptionHint()
        description_result = description_hint.apply(self)
        return description_result

    # 6. getting hints on image in the current game.
    # a string with a link will be returned
    def get_imageHint(self):
        image_hint = ImageHint()
        image_result = image_hint.apply(self)
        return image_result
    

    # we compare the string that the user entered with the title of the movie
    def is_same_film(self, user_input, threshold=80) -> bool:
        similarity = fuzz.partial_ratio(self.film[5], user_input)
        # Check if it is higher than the threshold value (80%)
        result = similarity >= threshold
        InsertGameData.insert_game_result(self, result)
        InsertGameData.insert_guessed_films(self, result)
        return result
