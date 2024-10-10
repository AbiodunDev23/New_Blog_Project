from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from .signals import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully {username}!')
            return redirect('login')
        else:
            messages.warning(request, 'Invalid Login Details..')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form' : form})


def login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} you are  logged in successfully!')
            messages.info(request, 'WELCOME TO BLOG_POST_WEBSITE||')
            return redirect('index')
        else:
            messages.warning(request, 'Invalid Login Details..')

    else:
        form = UserLoginForm()
    return render(request, 'login.html')
def logged(request):
    return render(request, 'logged.html')
def custom_logout_views(request):
    logout(request)
    return redirect('logged')
@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            user = u_form.cleaned_data.get('username')
            messages.success(request, 'Account Updated Successfully')
            return redirect('profile')
        else:
            messages.warning(request, f'Unable to Update  Your Account {user.username}')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
    }
    return render(request, 'profile.html', context)