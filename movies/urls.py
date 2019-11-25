from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/rating/', views.create_rating, name='rating'),
    path('<int:movie_pk>/rating/<int:rating_pk>/', views.delete_rating, name='delete_rating'),
    path('<int:movie_pk>/rating/<int:rating_pk>/update/', views.update_rating, name='update_rating'),
    path('<int:movie_pk>/like/', views.like, name='like')
]
