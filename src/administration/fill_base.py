from src.api.api_manager import ApiManager
from src.database.primary_filling_manager import PrimaryFillingManager



is_fill_genres = False  # or False, depending on your requirements
is_fill_films = False  # or False, depending on your requirements
is_fill_people = False  # or False, depending on your requirements
is_keywords = True  # or False, depending on your requirements

if is_fill_genres:
    data = ApiManager.get_genres()
    PrimaryFillingManager.fill_genres(data)
if is_fill_films:
    data = ApiManager.get_films()
    PrimaryFillingManager.fill_movies(data)
if is_fill_people:
    all_movies = PrimaryFillingManager.get_all_movies()
    for movie in all_movies:
        id_tmdb = movie[3]
        data = ApiManager.get_people(id_tmdb)
        PrimaryFillingManager.fill_people_and_related_data(id_tmdb, data)
if is_keywords:
    all_movies = PrimaryFillingManager.get_all_movies()
    for movie in all_movies:
        id_tmdb = movie[3]
        data = ApiManager.get_keywords(id_tmdb)
        PrimaryFillingManager.fill_keywords(id_tmdb, data)
        





