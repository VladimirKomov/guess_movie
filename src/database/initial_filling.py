
from primary_filling_manager import PrimaryFillingManager


data = PrimaryFillingManager.read_json('resources/genres.json')
PrimaryFillingManager.fill_genres(data)

data = PrimaryFillingManager.read_json('resources/films.json')
PrimaryFillingManager.fill_movies(data)

data = PrimaryFillingManager.read_json('resources/films.json')
PrimaryFillingManager.fill_genres_films(data)