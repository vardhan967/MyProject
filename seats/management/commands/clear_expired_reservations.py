# seats/management/commands/clear_expired_reservations.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from seats.models import Seat

class Command(BaseCommand):
    help = 'Clears expired seat reservations.'

    def handle(self, *args, **options):
        now = timezone.now()
        expired_seats = Seat.objects.filter(
            status='reserved',
            reserved_until__lt=now
        )
        count = 0
        for seat in expired_seats:
            seat.release()
            count += 1
            self.stdout.write(self.style.SUCCESS(f'Released expired reservation for Seat: {seat.name}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully cleared {count} expired seat reservations.'))