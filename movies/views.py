from django.http import JsonResponse, Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render,get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Movie, Rating
from .forms import RatingForm
import json
from random import choice, shuffle

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    if request.user.is_authenticated:
        if request.user.like_movies.all().count():
            last_like_movie = choice(request.user.like_movies.all())
            recommend_movies = list(Movie.objects.filter(genres=last_like_movie.genres.all()[0]).exclude(title=last_like_movie.title))
            shuffle(recommend_movies)
            context = {'movies': movies, 'last_like_movie':last_like_movie, 'recommend_movies':recommend_movies[:3],}
            return render(request, 'movies/index.html', context)
    
    context = {'movies': movies,}
    return render(request, 'movies/index.html', context)

    
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk) 
    movie.actors =  json.loads(movie.actors.replace("'", '"'))
    copy_actors = {}
    for actor,value in movie.actors.items():
        copy_actors[actor.replace('@', "'")] = [value[0].replace('@', "'").replace('%', '"'), value[1]]
    movie.actors = copy_actors
    form = RatingForm()
    ratings = movie.rating_set.all()
    context = {'movie':movie, 'form':form, 'ratings':ratings,}
    return render(request, 'movies/detail.html', context)

@require_POST
def create_rating(request, movie_pk):
    if request.user.is_authenticated:
        form = RatingForm(request.POST)
        if form.is_valid:
            #객체를 Create 하지만, db에 레코드는 작성하지 않는다.
            rating = form.save(commit=False)
            rating.movie_id = movie_pk
            rating.user = request.user
            rating.save()
    return redirect('movies:detail', movie_pk)

@require_POST
def delete_rating(request, movie_pk, rating_pk):
    if request.user.is_authenticated:
        rating = get_object_or_404(Rating, pk=rating_pk)
        if rating.user == request.user:
            rating.delete()
        return redirect('movies:detail', movie_pk)    
    return HttpResponse('You are Unauthorized', status=401)


@login_required
def update_rating(request, movie_pk, rating_pk):
    rating = get_object_or_404(Rating, pk=rating_pk)
    if request.user == rating.user:
        if request.method == 'POST':
            form = RatingForm(request.POST, instance=rating)
            if form.is_valid:            
                rating = form.save(commit=False)
                rating.movie_id = movie_pk
                rating.user = request.user
                rating.save()
                return redirect('movies:detail', movie_pk)  
        else:
            form = RatingForm(instance=rating)
    else:
        return redirect('movies:detail', movie_pk)    
    context = {'form':form, 'rating':rating,}
    return render(request, 'movies/update_rating.html', context)


@login_required
def like(request, movie_pk):
    if request.is_ajax():
        movie = get_object_or_404(Movie, pk=movie_pk)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
            liked = False
        else:
            movie.like_users.add(request.user)
            liked = True
        context = {'liked': liked, 'count': movie.like_users.count(),}
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest()