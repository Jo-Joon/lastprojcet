from django.http import JsonResponse, Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomUserChangeFormAdmin
from django.views.decorators.http import require_POST

# Create your views here.

User = get_user_model()

@staff_member_required
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
        form = CustomUserChangeFormAdmin(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')        
    else:
        form = CustomUserChangeFormAdmin(instance=person)
    context = {'form':form,}
    return render(request, 'accounts/auth_form.html', context)

def profile(request, username):
    person = get_object_or_404(User, username=username)
    context = {'person':person,}
    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, user_pk):
    if request.is_ajax():
        person = get_object_or_404(User, pk=user_pk)
        user = request.user
        # if person != user:
        if person.followers.filter(pk=user.pk).exists():
            person.followers.remove(user)
            followed = False
        else:
            person.followers.add(user)
            followed = True
        context = {'followed': followed, 'count': person.followers.count(),}
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest()


@require_POST
def delete_user(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('movies:index')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form,}
    return render(request, 'accounts/auth_form.html', context)

@login_required
def update_user(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')        
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form':form,}
    return render(request, 'accounts/auth_form.html', context)