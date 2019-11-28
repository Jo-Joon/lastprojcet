from django import forms
from .models import Rating, Movie
from django_starfield import Stars

INTEGER_CHOICES= [tuple([x,x]) for x in range(10, -1, -1)]

class RatingForm(forms.ModelForm):
    score = forms.IntegerField(widget=Stars)
    class Meta:
        model = Rating
        fields = ('score', 'comment',)

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = {'like_users'}