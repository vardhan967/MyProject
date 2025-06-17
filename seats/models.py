# seats/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Library Section/Room'
        verbose_name_plural = 'Library Sections/Rooms'

    def __str__(self):
        return self.name

class Seat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='seats')
    # Add 'pending_confirmation' as a possible status
    status = models.CharField(
        max_length=20,
        default='available',
        choices=[
            ('available', 'Available'),
            ('reserved', 'Reserved'), # This will now mean 'Confirmed Reserved'
            ('pending_confirmation', 'Pending Confirmation'), # New status
        ]
    )
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reserved_until = models.DateTimeField(null=True, blank=True)
    # A new field to mark if it's confirmed or not (could also use status, but this is explicit)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['location__name', 'name']
        verbose_name = 'Seat'
        verbose_name_plural = 'Seats'

    def __str__(self):
        return f"{self.name} ({self.location.name})"

    def is_available(self):
        # If pending_confirmation or reserved seat expires, make it available
        if self.status in ['reserved', 'pending_confirmation'] and \
           self.reserved_until and timezone.now() >= self.reserved_until:
            self.status = 'available'
            self.booked_by = None
            self.reserved_until = None
            self.is_confirmed = False # Reset confirmation status
            self.save()
            return True
        return self.status == 'available'

    def reserve(self, user):
        # This will now set the status to 'pending_confirmation'
        if self.is_available():
            self.status = 'pending_confirmation' # Initial status is pending
            self.booked_by = user
            self.reserved_until = timezone.now() + timedelta(minutes=10) # 10-min window for admin confirmation
            self.is_confirmed = False # Ensure it's not confirmed yet
            self.save()
            return True
        return False

    def release(self):
        if self.status in ['reserved', 'pending_confirmation']: # Can release either state
            self.status = 'available'
            self.booked_by = None
            self.reserved_until = None
            self.is_confirmed = False # Reset confirmation status
            self.save()
            return True
        return False

    def confirm_booking(self):
        # This method is called by the admin
        if self.status == 'pending_confirmation':
            self.status = 'reserved' # Now it's a confirmed reservation
            self.is_confirmed = True
            # Optionally extend reserved_until for confirmed bookings, e.g., to end of day
            # self.reserved_until = timezone.make_aware(timezone.datetime.combine(timezone.now().date(), timezone.time(23, 59, 59))) # Until end of day
            self.reserved_until = timezone.now() + timedelta(hours=4) # Example: 4 hours from confirmation
            self.save()
            return True
        return False

    def is_reserved_by_current_user(self, user):
        # This checks if it's either pending or confirmed by the user
        return self.booked_by == user and \
               self.status in ['reserved', 'pending_confirmation'] and \
               self.reserved_until and \
               timezone.now() < self.reserved_until