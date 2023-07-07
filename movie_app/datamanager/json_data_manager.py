import json

from flask_login import current_user

from movie_app.datamanager.data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    """ Represents a json file data manager """

    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self) -> dict[dict]:
        """
        Get all users from storage
        :return: dictionary containing the users
        """
        with open(self.filename) as handle:
            return json.loads(handle.read())

    def get_user_movies(self, email) -> list[dict]:
        """
        Get user's movie list
        :param email: email of the current user (used as an identifier)
        :return: list of movies
        """
        all_users = self.get_all_users()
        return all_users[email]['movies']

    def get_user_by_email(self, email) -> dict:
        """
        Find a user by email
        :param email: user's email (used as an identifier)
        :return: dictionary representing the user
        """
        return self.get_all_users().get(email)

    def find_movie_by_id(self, movie_id: int) -> dict:
        """
        Find movie by its id
        :param movie_id: identifier for a movie
        :return: dictionary representing the user
        """
        movies = self.get_user_movies(current_user.id)
        for movie in movies:
            if movie['id'] == movie_id:
                return movie

    def add_user(self, user: dict):
        """
        Add new user to storage
        :param user: user to be added
        """
        users = self.get_all_users()
        users.update(user)
        self._update_json_file(users)

    def add_movie(self, new_movie: dict):
        """
        Add new movie to a user's movie list
        :param new_movie: movie to be added
        """
        users = self.get_all_users()
        users[current_user.id]['movies'].append(new_movie)
        self._update_json_file(users)

    def update_movie(self, movie_id: int, updated_movie: dict):
        """
        Update movie's data
        :param movie_id: identifier for a movie
        :param updated_movie: dictionary representing the updated movie
        """
        users = self.get_all_users()
        for movie in users[current_user.id]['movies']:
            if movie['id'] == movie_id:
                movie.update(updated_movie)
                break
        self._update_json_file(users)

    def delete_movie(self, movie_id: int):
        """
        Delete a movie from a user's movie list
        :param movie_id: identifier for a movie
        """
        users = self.get_all_users()
        movie = self.find_movie_by_id(movie_id)
        users[current_user.id]['movies'].remove(movie)
        self._update_json_file(users)

    def _update_json_file(self, users: dict[dict]):
        """
        Update the json storage with new users data
        :param users: dictionary of users and their data
        """
        with open(self.filename, 'w') as handle:
            handle.write(json.dumps(users, indent=4))
