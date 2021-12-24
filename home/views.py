from django.shortcuts import render
import pip._vendor.requests

import random

from . import configuration as c
from . import movie as m

# Create your views here.

def search_with_config(request):
    if (not request.GET.get("director") and not request.GET.get("genre") and not print(request.GET.get("release_gte")) and not request.GET.get("release_lte")):
        return render(request, 'home/error.html')

    query = c.configuration(request.GET.get("genre"), request.GET.get("director"), request.GET.get("release_gte"), request.GET.get("release_lte"))

    try:
        results = query.get_movies()
    except:
        return render(request, 'home/error.html')

    return render(request, 'home/results.html', {
            "data" : results
    })

def search_random(request):
    page = random.randint(1, 14)
    data = pip._vendor.requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key=05e5be7a518e07b0cdd93bf0e133083a&language=en-US&include_adult=false&include_video=false&page={page}&primary_release_date.gte=1970&primary_release_date.lte=2010&release_date.gte=1970&release_date.lte=2000&vote_count.gte=1000&vote_average.gte=7.2&with_watch_monetization_types=flatrate")
    movies = []

    for movie in data.json()["results"]:
        mov = m.movie(movie["title"], movie["poster_path"], movie["id"])
        movies.append(mov)

    results = []
    
    while (len(results) < 4):
        index = random.randint(0, len(movies) - 1)
        if (movies[index].been == False):
            results.append(movies[index])
            movies[index].been = True
        else:
            continue

    return render(request, 'home/results.html', {
        "data": results
    })

def index(request):
    return render(request, 'home/main.html')