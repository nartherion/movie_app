import pip._vendor.requests

class movie:
    def __init__(self, t, pp, id):
        self.title = t
        self.poster_path = pp
        self.been = False
        self.imdb_id = pip._vendor.requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key=05e5be7a518e07b0cdd93bf0e133083a&language=en-US").json()["imdb_id"]