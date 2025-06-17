# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Roll Number", max_length=150)
    class Meta:
        model = User
        fields = ('username', 'password')