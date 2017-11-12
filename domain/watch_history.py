import time


from domain.movie import Movie


class WatchHistory:

    def __init__(self, user_id):
        self.user_id = user_id
        self.movies = {}

    def add_movie(self, movie_id):
        self.movies[movie_id] = Movie(movie_id, int(time.time()))


