from src.api.api_manager import ApiManager
from src.database.primary_filling_manager import PrimaryFillingManager


def fill_genres():
    data = ApiManager.get_genres()
    PrimaryFillingManager.fill_genres(data)

def fill_films():
    data = ApiManager.get_films()
    PrimaryFillingManager.fill_movies(data)

def fill_people():
    all_movies = PrimaryFillingManager.get_all_movies()
    for movie in all_movies:
        id_tmdb = movie[3]
        data = ApiManager.get_people(id_tmdb)
        PrimaryFillingManager.fill_people_and_related_data(id_tmdb, data)

def fill_keywords():
    all_movies = PrimaryFillingManager.get_all_movies()
    for movie in all_movies:
        id_tmdb = movie[3]
        data = ApiManager.get_keywords(id_tmdb)
        PrimaryFillingManager.fill_keywords(id_tmdb, data)

def fill_all_data_films_by_page(page):
    fill_genres()
    data = ApiManager.get_films(page)
    PrimaryFillingManager.fill_movies(data)
    for movie in data['results']:
        id_tmdb = movie['id']
        data = ApiManager.get_people(id_tmdb)
        PrimaryFillingManager.fill_people_and_related_data(id_tmdb, data)
        data = ApiManager.get_keywords(id_tmdb)
        PrimaryFillingManager.fill_keywords(id_tmdb, data)
    
    
    
        





