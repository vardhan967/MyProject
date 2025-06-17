# seat_booking_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect # Import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('seats/', include('seats.urls')),
    path('', lambda request: redirect('seats:seat_dashboard')), # <--- CHANGED HERE
     path('api/', include('api.urls')),

]