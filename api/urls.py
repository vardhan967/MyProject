# api/urls.py

from django.urls import path, include

urlpatterns = [
    path('seats/', include('seats.api_urls')),
    path('auth/', include('accounts.api_urls')),
]