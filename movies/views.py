from django.shortcuts import render,get_object_or_404
from .models import Movie
import json

# Create your views here.
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)   
    movie.actors = json.loads(movie.actors.replace("'", "\""))
    context = {'movie':movie}
    return render(request, 'movies/detail.html', context)