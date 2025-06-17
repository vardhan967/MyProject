# seats/serializers.py

from rest_framework import serializers
from .models import Seat, Location
from accounts.serializers import UserSerializer

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'description']

class SeatSerializer(serializers.ModelSerializer):
    # Use our UserSerializer to show nested user data
    booked_by = UserSerializer(read_only=True)
    # Use a SerializerMethodField to get a clean location name
    location_name = serializers.CharField(source='location.name', read_only=True)

    class Meta:
        model = Seat
        fields = [
            'id',
            'name',
            'location',
            'location_name',
            'status',
            'booked_by',
            'reserved_until',
            'is_confirmed',
        ]