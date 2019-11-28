from django.db import models
from django.conf import settings
from django.core.validators import validate_comma_separated_integer_list, MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import JSONField

class Genre(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class Movie(models.Model):
    movie_cd = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    title_en = models.CharField(max_length=150)
    audience = models.IntegerField()
    summary = models.TextField(blank=True)
    poster_url = models.TextField(blank=True)
    backdrop_url = models.TextField(blank=True)
    directors = models.CharField(max_length=500, blank=True)
    release_date = models.DateField(blank=True)
    actors = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    rate = models.CharField(max_length=50, blank=True)
    running_time = models.CharField(max_length=50, blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)
    class Meta:
        ordering = ('-pk',)
    def __str__(self):
        return self.title    

class Rating(models.Model):
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.CharField(max_length=150)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    update_at = models.DateTimeField(auto_now=True)

