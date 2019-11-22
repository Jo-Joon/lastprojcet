from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Create your views here.

User = get_user_model()

def index(request):
    people = User.objects.all()
    context = {'people':people,}
    return render(request, 'accounts/index.html', context)

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    context = {'form':form,}
    return render(request, 'accounts/auth_form.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'accounts:index')
    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'accounts/login_form.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:index')

@staff_member_required
def delete(request, user_pk):
    del_user = get_object_or_404(User, pk=user_pk)
    del_user.delete()
    return redirect('accounts:index')

@staff_member_required
def update(request, user_pk):
    person = get_object_or_404(User, pk=user_pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')        
    else:
        form = CustomUserChangeForm(instance=person)
    context = {'form':form,}
    return render(request, 'accounts/auth_form.html', context)