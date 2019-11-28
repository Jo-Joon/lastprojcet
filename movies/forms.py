from django import forms
from .models import Rating, Movie

INTEGER_CHOICES= [tuple([x,x]) for x in range(10, -1, -1)]

class RatingForm(forms.ModelForm):
    score = forms.IntegerField(min_value=0, max_value=10, widget=forms.Select(choices=INTEGER_CHOICES))
    class Meta:
        model = Rating
        fields = ('score', 'comment',)

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = {'like_users'}