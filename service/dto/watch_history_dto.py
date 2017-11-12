from service.dto.movie_dto import MovieDto


class WatchHistoryDto:
    @staticmethod
    def create(watch_history):
        return list(map(
            lambda movie_id: MovieDto().create(watch_history.movies[movie_id]),
            watch_history.movies))
