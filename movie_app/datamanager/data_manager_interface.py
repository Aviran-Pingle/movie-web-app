from abc import ABC, abstractmethod
from typing import Any


class DataManagerInterface(ABC):
    """ Interface for storage data managers """
    @abstractmethod
    def get_all_users(self):
        """
        Get all users from storage
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id: Any):
        """
        Get movies of a given user
        :param user_id: a unique identifier (of any type)
        """
        pass

    @abstractmethod
    def add_user(self, new_user):
        """
        Add new user to storage
        :param new_user: new user to be added
        """
        pass

    @abstractmethod
    def add_movie(self, new_movie):
        """
        Add new movie to a specific user's list
        :param new_movie: movie to be added
        """
        pass

    @abstractmethod
    def update_movie(self, movie_id: int, updated_movie):
        """
        Update a given movie's data
        :param movie_id: identifier for a movie
        :param updated_movie: obj representing the updated movie
        """
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """
        Delete a movie from storage
        :param movie_id: identifier for a movie
        """
        pass
