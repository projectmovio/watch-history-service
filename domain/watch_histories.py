from domain.watch_history import WatchHistory


class WatchHistories:

    def __init__(self):
        self.watch_histories = {}

    def get_watch_history(self, user_id):
        if user_id not in self.watch_histories:
            self.watch_histories[user_id] = WatchHistory(user_id)

        return self.watch_histories[user_id]


