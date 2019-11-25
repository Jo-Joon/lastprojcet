from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete_user, name='delete_user'),
    path('password/', views.change_password, name='password'),
    path('update/', views.update_user, name='update_user'),
    path('delete/<int:user_pk>/', views.delete, name='delete'),
    path('update/<int:user_pk>/', views.update, name='update'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('<username>/', views.profile, name='profile'),
]
