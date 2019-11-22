from django.contrib import admin
from . models import Rating, Movie, Genre
# Register your models here.
admin.site.register(Rating)
admin.site.register(Movie)
admin.site.register(Genre)