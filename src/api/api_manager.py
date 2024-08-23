import json
import os
import requests
import configparser

class ApiManager:
    # to access the configuration file
    config = configparser.ConfigParser()
    script_dir = os.path.dirname(__file__)
    config.read(script_dir + "/config_api.ini")
    token = f"Bearer {config['api']['token']}" # A token is generated here

#   Get a list of movies ordered by rating.
    @staticmethod
    def get_films(page) -> dict:
        try:
            url = f"{ApiManager.config['api']['url']}/movie/top_rated?language=en-US&page={page}"
            headers = {
                "accept": "application/json",
                "Authorization": ApiManager.token
            }
            response = requests.get(url, headers=headers)

            films = response.json()

            return films
        except requests.exceptions.RequestException as e:
            print(f'Error loading films: {e}')
            return []

# Get the list of official genres for movies
    @staticmethod
    def get_genres() -> dict:
        try:
            url = f"{ApiManager.config['api']['url']}/genre/movie/list?language=en"
            headers = {
                "accept": "application/json",
                "Authorization": ApiManager.token
            }
            response = requests.get(url, headers=headers)
            genres = response.json()

            return genres
        
        except requests.exceptions.RequestException as e:
            print(f'Error loading genres: {e}')
            return []
      
# Gets the entire cast for the movie by id
    @staticmethod
    def get_people(film_id) -> dict:
        try:
            url = f"{ApiManager.config['api']['url']}/movie/{film_id}/credits"
            headers = {
            "accept": "application/json",
            "Authorization": ApiManager.token
            }
            response = requests.get(url, headers=headers)
            people = response.json()
  
            return people
        except requests.exceptions.RequestException as e:
            print(f'Error loading actors for movie ID {film_id}: {e}')
            return []  
        

    #  Get the list of keywords for the movie by id
    @staticmethod    
    def get_keywords(film_id) -> dict:
        try:
            url = f"{ApiManager.config['api']['url']}/movie/{film_id}/keywords"
            headers = {
            "accept": "application/json",
            "Authorization": ApiManager.token
             }
            response = requests.get(url, headers=headers)
            keywords = response.json()
     
            return keywords
        except requests.exceptions.RequestException as e:
             print(f'Error loading keywords for movie ID {film_id}: {e}')
             return []  
    
    
