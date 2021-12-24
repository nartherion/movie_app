import pip._vendor.requests

from . import movie as m

TMDB_API_KEY = "05e5be7a518e07b0cdd93bf0e133083a"

class configuration :
    __genre_id = 0
    __director_id = 0

    def __init__(self, g, d, y_gte, y_lte) :
        self.__genre = g
        self.__director = d
        self.__year_gte = y_gte
        self.__year_lte = y_lte

    def __find_genre_id(self):
        genre_list = pip._vendor.requests.get(f"https://api.themoviedb.org/3/genre/movie/list?api_key=05e5be7a518e07b0cdd93bf0e133083a&language=en-US")
        for g in genre_list.json()["genres"]:
            if (g["name"] == self.__genre):
                self.__genre_id = g["id"]
                break
        
        if (self.__genre_id == 0):
            raise Exception("Bad_query")

    def __find_director_id(self):
        director_name = self.__director.split(' ')[0]
        director_surname = self.__director.split(' ')[1]
        self.__director_id = pip._vendor.requests.get(f"https://api.themoviedb.org/3/search/person?api_key=05e5be7a518e07b0cdd93bf0e133083a&language=en-US&query={director_name}%20{director_surname}&page=1&include_adult=false").json()["results"][0]["id"]
        
    def __proof_directed(self, movie_id):
        movie_credits = pip._vendor.requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=05e5be7a518e07b0cdd93bf0e133083a&language=en-US").json()["crew"]
        for mc in movie_credits:
            if ( (mc["id"] == self.__director_id) and (mc["job"] == "Director") ):
                return True
        return False

    def __construct_query(self):
        request_string = "https://api.themoviedb.org/3/discover/movie?api_key=" + TMDB_API_KEY
        request_string += "&language=en-US" 
        request_string += "&sort_by=popularity.desc"
        request_string += "&include_adult=false"
        request_string += "&include_video=false"
        request_string += "&page=1"

        if ((self.__year_gte and self.__year_lte) and (self.__year_lte >= self.__year_gte)):
            request_string += "&primary_release_date.gte=" + str(self.__year_gte) + "&primary_release_date.lte=" + str(self.__year_lte)
            request_string += "&release_date.gte=" + str(self.__year_gte) + "&release_date.lte=" + str(self.__year_lte)

        if (self.__director and self.__genre):
            self.__find_director_id()
            self.__find_genre_id()
            request_string += "&with_crew=" + str(self.__director_id)
            request_string += "&with_genres=" + str(self.__genre_id)
        elif (self.__director and (not self.__genre)):
            self.__find_director_id()
            request_string += "&with_crew=" + str(self.__director_id)
        elif ((not self.__director) and self.__genre):
            self.__find_genre_id()
            request_string += "&with_genres=" + str(self.__genre_id)

        request_string += "&with_watch_monetization_types=flatrate"

        return request_string

    def get_movies(self):
        movies = []

        if (self.__director):
            data = pip._vendor.requests.get(f"{self.__construct_query()}")

            for movie in data.json()["results"]:
                if (self.__proof_directed(movie['id'])):
                    temp = m.movie(movie["title"], movie["poster_path"], movie["id"])
                    movies.append(temp)
                else:
                    continue
        else:
            data = pip._vendor.requests.get(f"{self.__construct_query()}")

            for movie in data.json()["results"]:
                temp = m.movie(movie["title"], movie["poster_path"], movie["id"])
                movies.append(temp)

        return movies