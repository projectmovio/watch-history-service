class MovieDto:

    @staticmethod
    def create(movie):
        return {"movie_id": movie.movie_id, "watch_date": movie.watch_date}
