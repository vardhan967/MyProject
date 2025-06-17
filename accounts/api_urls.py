# accounts/api_urls.py

from django.urls import path
from .views import CurrentUserAPIView, CSRFTokenAPIView
# We'll use the existing template-based login/logout views which work fine with session auth
from . import views as auth_views

app_name = 'accounts_api'

urlpatterns = [
    # Use existing views for login/logout, they set the session cookie
    path('login/', auth_views.user_login, name='login'),
    path('logout/', auth_views.user_logout, name='logout'),

    # API endpoints
    path('user/', CurrentUserAPIView.as_view(), name='current-user'),
    path('csrf-token/', CSRFTokenAPIView.as_view(), name='csrf-token'),
    
]