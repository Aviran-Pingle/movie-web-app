from movie_app.datamanager.models import User, Movie, Review
from movie_app.datamanager.data_manager_interface import DataManagerInterface
from movie_app.movies.forms import UpdateMovieForm


class SQLiteDataManager(DataManagerInterface):
    """
    Implementation of the DataManagerInterface using SQLite database.
    """
    def __init__(self, db):
        """
        Initialize the SQLiteDataManager.
        :param db: the SQLAlchemy database instance.
        """
        self.db = db

    def get_all_users(self):
        """
        Retrieve a list of all users in the database.
        :return: a list of User objects representing all users in the database.
        """
        return User.query.all()

    def get_user_movies(self, user_id: int):
        """
        Retrieve movies associated with a specific user.
        :param user_id: the ID of the user.
        :return: a list of Movie objects associated with the specified user.
        """
        user = User.query.get(user_id)
        return user.movies

    def add_user(self, new_user):
        """
        Add a new user to the database.
        :param new_user: the User object to be added to the database.
        """
        self.db.session.add(new_user)
        self.db.session.commit()

    def add_movie(self, new_movie):
        """
        Add a new movie to the database.
        :param new_movie: the Movie object to be added to the database.
        """
        self.db.session.add(new_movie)
        self.db.session.commit()

    def update_movie(self, movie_id: int, form: UpdateMovieForm):
        """
        Update movie details in the database.
        :param movie_id: the ID of the movie to be updated.
        :param form: the form containing updated movie information.
        """
        movie = Movie.query.get(movie_id)
        movie.director = form.director.data
        movie.year = form.year.data
        movie.rating = form.rating.data
        self.db.session.commit()

    def delete_movie(self, movie_id):
        """
        Delete a movie from the database.
        :param movie_id: the ID of the movie to be deleted.
        """
        movie = Movie.query.get(movie_id)
        self.db.session.delete(movie)
        self.db.session.commit()

    @staticmethod
    def find_movie_by_id(movie_id):
        """
        Retrieve a movie by its ID.
        :param movie_id: the ID of the movie to retrieve.
        :return: the Movie object corresponding to the given ID.
        """
        return Movie.query.get(movie_id)

    @staticmethod
    def get_user_email(user_id):
        """
        Retrieve the email address of a user.
        :param user_id: the ID of the user.
        :return: the email address of the user.
        """
        return User.query.get(user_id).email

    def add_review(self, text, movie_id):
        """
        Add a new review for a movie.
        :param text: content of the review.
        :param movie_id: ID of the movie for which the review is being added.
        """
        self.db.session.add(Review(text=text, movie_id=movie_id))
        self.db.session.commit()

    def update_review(self, review_id, text):
        """
        Update the content of an existing review.
        :param review_id: the ID of the review to be updated.
        :param text: the new content for the review.
        """
        review = Review.query.get(review_id)
        if review.text != text:
            review.text = text
            self.db.session.commit()

    def delete_review(self, review_id):
        """
         Delete a review.
        :param review_id: the ID of the review to be deleted.
        """
        review = Review.query.get(review_id)
        self.db.session.delete(review)
        self.db.session.commit()
