# seats/admin.py
from django.contrib import admin
from .models import Seat, Location

# Register your models here.
admin.site.register(Location) # Register the new Location model

@admin.register(Seat) # Use decorator for Seat
class SeatAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'status', 'booked_by', 'reserved_until_display')
    list_filter = ('location', 'status') # Add location to filters
    search_fields = ('name', 'location__name') # Search by seat name or location name
    raw_id_fields = ('booked_by',) # For better user selection in admin
 
    def reserved_until_display(self, obj):
        if obj.reserved_until:
            return obj.reserved_until.strftime('%Y-%m-%d %H:%M:%S')
        return "-"
    reserved_until_display.short_description = 'Reserved Until'
    reserved_until_display.admin_order_field = 'reserved_until'