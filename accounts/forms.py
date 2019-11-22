from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()  # return User
        fields = ('email', 'is_staff', )

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model() #account.User
        fields = UserCreationForm.Meta.fields + ('email', )