# seats/urls.py

from django.urls import path
from . import views

app_name = 'seats' # This is important for namespacing

urlpatterns = [
    path('', views.seat_dashboard, name='seat_dashboard'),
    path('book/<int:seat_id>/', views.book_seat, name='book_seat'),
    path('release/<int:seat_id>/', views.release_seat, name='release_seat'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    # New Admin Check-in URLs
    path('admin/checkin/', views.admin_checkin_dashboard, name='admin_checkin_dashboard'),
    path('admin/confirm/<int:seat_id>/', views.confirm_seat_booking, name='confirm_seat_booking'),
]