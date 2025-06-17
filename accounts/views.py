# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages
from rest_framework import views, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('seats:seat_list')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('seats:seat_dashboard')
            else:
                messages.error(request, 'Invalid Roll Number or Password.')
        else:
            messages.error(request, 'Invalid Roll Number or Password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

class CurrentUserAPIView(views.APIView):
    """API endpoint to get the current logged-in user's details."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class CSRFTokenAPIView(views.APIView):
    """
    API endpoint to provide a CSRF token to the frontend.
    React will call this first before any POST/PATCH/DELETE request.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Django's get_token function will set the csrftoken cookie
        from django.middleware.csrf import get_token
        get_token(request)
        return Response({"detail": "CSRF cookie set."})