from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from .models import profile
from django import forms
class UserRegistrationForm(UserCreationForm):
    email = models.EmailField(null=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    

class UserLoginForm(UserCreationForm):
    email = models.EmailField(null=False)
    class Meta:
        model = User
        fields = ['username']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['image']