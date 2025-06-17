# seats/api_urls.py

from django.urls import path
from .views import (
    LocationListAPIView,
    SeatListAPIView,
    BookSeatAPIView,
    ReleaseSeatAPIView,
    MyReservationsAPIView,
    PendingSeatsAPIView,
    ConfirmSeatAPIView,
)

app_name = 'seats_api'

urlpatterns = [
    # Public endpoints
    path('locations/', LocationListAPIView.as_view(), name='location-list'),
    path('', SeatListAPIView.as_view(), name='seat-list'),

    # User-specific actions
    path('<int:seat_id>/book/', BookSeatAPIView.as_view(), name='seat-book'),
    path('<int:seat_id>/release/', ReleaseSeatAPIView.as_view(), name='seat-release'),
    path('my-reservations/', MyReservationsAPIView.as_view(), name='my-reservations'),

    # Admin actions
    path('admin/pending/', PendingSeatsAPIView.as_view(), name='admin-pending-list'),
    path('admin/<int:seat_id>/confirm/', ConfirmSeatAPIView.as_view(), name='admin-seat-confirm'),
]