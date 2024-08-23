import json
import os
import requests
import configparser


class ApiManager:
    # to access the configuration file
    config = configparser.ConfigParser()
    script_dir = os.path.dirname(__file__)
    config.read(script_dir + "/config_database.ini")
    token = f"Bearer {config['api']['token']}"  # A token is generated here

    #   Get a list of movies ordered by rating.
    @staticmethod
    def _get_films(page) -> dict:
        try:
            url = f"{ApiManager.config['api']['url']}/movie/top_rated?language=en-US&page={page}"
            headers = {"accept": "application/json", "Authorization": ApiManager.token}
            response = requests.get(url, headers=headers)

            films = response.json()

            with open("films.json", "w") as f:
                json.dump(films, f, indent=4)

            return films
        except requests.exceptions.RequestException as e:
            print(f"Error loading films: {e}")
            return []

    # Get the list of official genres for movies
    @staticmethod
    def _get_genres() -> dict:
        try:
            url = f"{ApiManager.config['api']['url']}/genre/movie/list?language=en"
            headers = {"accept": "application/json", "Authorization": ApiManager.token}
            response = requests.get(url, headers=headers)
            genres = response.json()

            with open("genres.json", "w") as f:
                json.dump(genres, f, indent=4)
            return genres

        except requests.exceptions.RequestException as e:
            print(f"Error loading genres: {e}")
            return []

    # Gets the entire cast for the movie by id
    @staticmethod
    def _get_people(film_id) -> dict:
        try:
            url = f"{ApiManager.config['api']['url']}/movie/{film_id}/credits"
            headers = {"accept": "application/json", "Authorization": ApiManager.token}
            response = requests.get(url, headers=headers)
            people = response.json()
            with open("people.json", "w") as f:
                json.dump(people, f, indent=4)
            return people
        except requests.exceptions.RequestException as e:
            print(f"Error loading actors for movie ID {film_id}: {e}")
            return []

    #  Get the list of keywords for the movie by id
    @staticmethod
    def _get_keywords(film_id) -> dict:
        try:
            url = f"{ApiManager.config['api']['url']}/movie/{film_id}/keywords"
            headers = {"accept": "application/json", "Authorization": ApiManager.token}
            response = requests.get(url, headers=headers)
            keywords = response.json()
            with open("keywords.json", "w") as f:
                json.dump(keywords, f, indent=4)
            return keywords
        except requests.exceptions.RequestException as e:
            print(f"Error loading keywords for movie ID {film_id}: {e}")
            return []


# ApiManager._get_films(1)
# ApiManager._get_genres()
# ApiManager._get_people(278)
ApiManager._get_keywords(278)
