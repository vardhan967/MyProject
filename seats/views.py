# seats/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from .models import Seat, Location
from django.db.models import Q
from django.contrib.auth import get_user_model # Import get_user_model
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .serializers import SeatSerializer, LocationSerializer
from django.db.models import Q
from django.utils import timezone

User = get_user_model() # Get your custom User model

# Helper function to check if user is staff/admin
def is_admin(user):
    return user.is_staff

@login_required
def seat_dashboard(request):
    # Auto-release expired seats before fetching and filtering
    all_seats = Seat.objects.all()
    for seat in all_seats:
        seat.is_available() # This will update status based on reserved_until

    seats = Seat.objects.all()

    query = request.GET.get('q')
    if query:
        seats = seats.filter(
            Q(name__icontains=query) |
            Q(location__name__icontains=query)
        ).distinct()

    status_filter = request.GET.get('status')
    if status_filter:
        seats = seats.filter(status=status_filter)

    location_filter = request.GET.get('location')
    if location_filter:
        seats = seats.filter(location__name__icontains=location_filter)

    seats = seats.order_by('location__name', 'name')

    context = {
        'seats': seats,
        'query': query,
        'current_status_filter': status_filter,
        'current_location_filter': location_filter,
        'locations': Location.objects.all().order_by('name'),
    }
    return render(request, 'seats/seat_list.html', context)


@login_required
def book_seat(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)

    if request.method == 'POST':
        # Check if user already has a pending or confirmed reservation
        user_active_seat = Seat.objects.filter(
            booked_by=request.user,
            status__in=['reserved', 'pending_confirmation'],
            reserved_until__gt=timezone.now()
        ).first()

        if user_active_seat:
            messages.warning(request, f"You already have Seat {user_active_seat.name} reserved or pending confirmation. Please manage that reservation first.")
            return redirect('seats:seat_dashboard')

        if seat.is_available(): # Will also clean up expired seats
            if seat.reserve(request.user): # This now sets status to 'pending_confirmation'
                my_reservations_url = reverse('seats:my_reservations')
                messages.success(request, f'Seat {seat.name} is now pending confirmation for 10 minutes! Please report to the admin. <a href="{my_reservations_url}" class="alert-link">Check your reservations here.</a>')
            else:
                messages.error(request, f'Seat {seat.name} is no longer available.')
        else:
            messages.error(request, f'Seat {seat.name} is currently reserved or pending confirmation by someone else.')
    return redirect('seats:seat_dashboard')

@login_required
def release_seat(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)

    if request.method == 'POST':
        if seat.is_reserved_by_current_user(request.user): # This checks for both 'reserved' and 'pending_confirmation'
            seat.release()
            messages.info(request, f"Seat {seat.name} has been released.")
        else:
            messages.error(request, f"You cannot release Seat {seat.name}.")
    return redirect('seats:seat_dashboard')

@login_required
def my_reservations(request):
    user_reserved_seats = Seat.objects.filter(
        booked_by=request.user,
        status__in=['reserved', 'pending_confirmation'], # Include both types
        reserved_until__gt=timezone.now()
    ).order_by('name')

    for seat in user_reserved_seats:
        seat.is_available() # Ensure status is updated for display

    # Re-fetch after potential updates by is_available
    user_reserved_seats = Seat.objects.filter(
        booked_by=request.user,
        status__in=['reserved', 'pending_confirmation'],
        reserved_until__gt=timezone.now()
    ).order_by('name')

    return render(request, 'seats/my_reservations.html', {'user_reserved_seats': user_reserved_seats})

# NEW ADMIN CHECK-IN VIEWS

@login_required
@user_passes_test(is_admin) # Only staff users can access this page
def admin_checkin_dashboard(request):
    # Get seats that are pending confirmation
    pending_seats = Seat.objects.filter(
        status='pending_confirmation',
        reserved_until__gt=timezone.now() # Ensure they haven't expired yet
    ).order_by('reserved_until', 'name') # Order by earliest expiration first

    context = {
        'pending_seats': pending_seats,
    }
    return render(request, 'seats/admin_checkin_dashboard.html', context)

@login_required
@user_passes_test(is_admin) # Only staff users can confirm bookings
def confirm_seat_booking(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)

    if request.method == 'POST':
        roll_number = request.POST.get('roll_number') # Get the roll number from the form

        if not roll_number:
            messages.error(request, "Roll number is required to confirm the booking.")
            return redirect('seats:admin_checkin_dashboard')

        # Assuming roll_number is the same as the username
        try:
            student_user = User.objects.get(username=roll_number)
        except User.DoesNotExist:
            messages.error(request, f"No student found with roll number: {roll_number}")
            return redirect('seats:admin_checkin_dashboard')

        # Check if the seat is indeed pending confirmation and booked by this student
        if seat.status == 'pending_confirmation' and seat.booked_by == student_user and timezone.now() < seat.reserved_until:
            if seat.confirm_booking():
                messages.success(request, f"Seat {seat.name} confirmed for {student_user.username}!")
            else:
                messages.error(request, f"Could not confirm seat {seat.name}.")
        else:
            messages.error(request, f"Seat {seat.name} is not pending confirmation for {roll_number} or has expired.")

    return redirect('seats:admin_checkin_dashboard')



class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class LocationListAPIView(generics.ListAPIView):
    """API endpoint to list all locations."""
    queryset = Location.objects.all().order_by('name')
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny] # Anyone can see locations

class SeatListAPIView(generics.ListAPIView):
    """
    API endpoint to list all seats.
    Can be filtered with query parameters: ?location_id=1&status=available
    """
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny] # Anyone can see the seat map

    def get_queryset(self):
        # Run the cleanup logic on every request to this endpoint
        for seat in Seat.objects.filter(status__in=['reserved', 'pending_confirmation']):
            seat.is_available()

        queryset = Seat.objects.select_related('location', 'booked_by').all()
        location_id = self.request.query_params.get('location_id')
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset.order_by('location__name', 'name')

class BookSeatAPIView(views.APIView):
    """API endpoint for a user to book a seat."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, seat_id, *args, **kwargs):
        seat = get_object_or_404(Seat, id=seat_id)

        # Check if user already has an active reservation
        user_active_seat = Seat.objects.filter(
            booked_by=request.user,
            status__in=['reserved', 'pending_confirmation'],
            reserved_until__gt=timezone.now()
        ).first()

        if user_active_seat:
            return Response(
                {"detail": f"You already have Seat {user_active_seat.name} reserved or pending. Please manage that reservation first."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if seat.is_available():
            if seat.reserve(request.user):
                serializer = SeatSerializer(seat)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # This case is unlikely if is_available is true, but good for safety
                return Response({"detail": "Failed to reserve seat due to an unexpected issue."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Seat is not available."}, status=status.HTTP_400_BAD_REQUEST)

class ReleaseSeatAPIView(views.APIView):
    """API endpoint for a user to release their own seat."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, seat_id, *args, **kwargs):
        seat = get_object_or_404(Seat, id=seat_id)
        if seat.is_reserved_by_current_user(request.user):
            seat.release()
            return Response({"detail": "Seat released successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You do not have permission to release this seat."}, status=status.HTTP_403_FORBIDDEN)

class MyReservationsAPIView(generics.ListAPIView):
    """API endpoint for a user to see their active reservations."""
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Run cleanup first
        for seat in Seat.objects.filter(booked_by=self.request.user):
            seat.is_available()
            
        return Seat.objects.filter(
            booked_by=self.request.user,
            status__in=['reserved', 'pending_confirmation'],
            reserved_until__gt=timezone.now()
        ).order_by('name')

# --- ADMIN API VIEWS ---

class PendingSeatsAPIView(generics.ListAPIView):
    """(Admin) API endpoint to list all seats pending confirmation."""
    serializer_class = SeatSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Seat.objects.filter(
            status='pending_confirmation',
            reserved_until__gt=timezone.now()
        ).select_related('location', 'booked_by').order_by('reserved_until')

class ConfirmSeatAPIView(views.APIView):
    """(Admin) API endpoint to confirm a pending booking."""
    permission_classes = [IsAdminUser]

    def post(self, request, seat_id, *args, **kwargs):
        seat = get_object_or_404(Seat, id=seat_id)
        if seat.status != 'pending_confirmation':
            return Response({"detail": "This seat is not pending confirmation."}, status=status.HTTP_400_BAD_REQUEST)
        
        if seat.confirm_booking():
            serializer = SeatSerializer(seat)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Failed to confirm booking."}, status=status.HTTP_400_BAD_REQUEST)