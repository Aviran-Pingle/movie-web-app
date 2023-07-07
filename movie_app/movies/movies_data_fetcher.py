import os

import requests

API_URL = f"http://www.omdbapi.com/"


def fetch_movie_data(movie_name: str) -> dict:
    """
    fetches data from an API
    :param movie_name: movie to be fetched
    :return: a dictionary with the fetched data,
    empty dict in case of a connection error
    """
    params = {"apikey": os.getenv("api_key"), "t": movie_name}
    try:
        movie_data = requests.get(API_URL, params=params)
    except requests.ConnectionError:
        return {}
    else:
        return movie_data.json()

