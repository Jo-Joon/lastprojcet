from django.http import JsonResponse, Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render,get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Movie, Rating
from .forms import RatingForm, MovieForm
import json
from random import choice, shuffle

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    genre_list = ['전체보기', '액션', '모험', '애니메이션', '코미디', '범죄', '다큐멘터리', '드라마', '가족', '판타지', '역사', '공포', '음악', '미스터리', '로맨스', 'SF', 'TV 영화', '스릴러', '전쟁', '서부']
    if request.user.is_authenticated:
        if request.user.like_movies.all().count():
            last_like_movie = choice(request.user.like_movies.all())
            recommend_movies = list(Movie.objects.filter(genres=last_like_movie.genres.all()[0]).exclude(title=last_like_movie.title))
            shuffle(recommend_movies)
            context = {'movies': movies, 'last_like_movie':last_like_movie, 'recommend_movies':recommend_movies[:3], 'genre_list': genre_list,}
            return render(request, 'movies/index.html', context)
    
    context = {'movies': movies, 'genre_list': genre_list,}
    return render(request, 'movies/index.html', context)

    
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk) 
    movie.actors =  json.loads(movie.actors.replace("'", '"'))
    copy_actors = {}
    for actor,value in movie.actors.items():
        copy_actors[actor.replace('@', "'")] = [value[0].replace('@', "'").replace('%', '"'), value[1]]
    movie.actors = copy_actors
    movie.directors = json.loads(movie.directors.replace("'", '"'))
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
    movie = get_object_or_404(Movie, pk=movie_pk)
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
    context = {'form':form, 'movie':movie, }
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


def genre_movie(request, genre_nm):
    movies = Movie.objects.all()
    genre_list = ['전체보기', '액션', '모험', '애니메이션', '코미디', '범죄', '다큐멘터리', '드라마', '가족', '판타지', '역사', '공포', '음악', '미스터리', '로맨스', 'SF', 'TV 영화', '스릴러', '전쟁', '서부']
    genre_movies = []
    if genre_nm != '전체보기':
        for movie in movies:
            for genre in movie.genres.all():
                if str(genre) == str(genre_nm):
                    genre_movies.append(movie)
    else:
        genre_movies = movies
    if request.user.is_authenticated:
        if request.user.like_movies.all().count():
            last_like_movie = choice(request.user.like_movies.all())
            recommend_movies = list(Movie.objects.filter(genres=last_like_movie.genres.all()[0]).exclude(title=last_like_movie.title))
            shuffle(recommend_movies)
            context = {'movies': genre_movies, 'last_like_movie':last_like_movie, 'recommend_movies':recommend_movies[:3], 'genre_list': genre_list,}
            return render(request, 'movies/index.html', context)
    context = {'movies': genre_movies, 'genre_list': genre_list}
    return render(request, 'movies/index.html', context)


def search_movie(request):
    movies = Movie.objects.all()
    genre_list = ['전체보기', '액션', '모험', '애니메이션', '코미디', '범죄', '다큐멘터리', '드라마', '가족', '판타지', '역사', '공포', '음악', '미스터리', '로맨스', 'SF', 'TV 영화', '스릴러', '전쟁', '서부']
    search_word = request.POST['search']
    movie_list = []
    for movie in movies:
        if search_word in movie.title:
            movie_list.append(movie)
    if request.user.is_authenticated:
        if request.user.like_movies.all().count():
            last_like_movie = choice(request.user.like_movies.all())
            recommend_movies = list(Movie.objects.filter(genres=last_like_movie.genres.all()[0]).exclude(title=last_like_movie.title))
            shuffle(recommend_movies)
            context = {'movies': movie_list, 'last_like_movie':last_like_movie, 'recommend_movies':recommend_movies[:3], 'genre_list': genre_list,}
            return render(request, 'movies/index.html', context)
    context = {'movies': movie_list}
    return render(request, 'movies/index.html', context)


@login_required
def create_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'movies/index.html')
    else:
        form = MovieForm()
    context = {'form': form,}
    return render(request, 'movies/form.html', context)


@login_required
def update_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie.save()
            return redirect('movies:detail', movie_pk)
    else:
        form = MovieForm(instance=movie)
    context = {'form': form, 'movie': movie}
    return render(request, 'movies/form.html', context)