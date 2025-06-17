import os
from django.core.management.base import BaseCommand
# CHANGE THIS LINE: Import 'Location' instead of 'LibrarySection'
from seats.models import Location, Seat 

class Command(BaseCommand):
    help = 'Populates the database with initial library sections and seats.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))

        # Data to be added
        sections_data = {
            'Central Library': 86,
            'GD - EAST': 4,
            'GD - WEST': 4,
            'Reference Section': 50,
            'Resource Center': 40,
        }

        for section_name, num_seats in sections_data.items():
            # CHANGE THIS LINE: Use Location.objects.get_or_create
            section, created = Location.objects.get_or_create(name=section_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Library Section/Room: {section_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Library Section/Room "{section_name}" already exists.'))

            # Create seats for the section
            for i in range(1, num_seats + 1):
                # You might want a more sophisticated naming convention for seats
                # e.g., "CL-001", "GD-EAST-A", etc.
                if section_name == 'Central Library':
                    seat_name = f"CL-{i:03d}"
                elif section_name == 'Reference Section':
                    seat_name = f"RS-{i:02d}"
                elif section_name == 'Resource Center':
                    seat_name = f"RC-{i:02d}"
                elif section_name == 'GD - EAST':
                    seat_name = f"GD-EAST-{chr(64 + i)}" # A, B, C, D
                elif section_name == 'GD - WEST':
                    seat_name = f"GD-WEST-{chr(64 + i)}" # A, B, C, D
                else:
                    seat_name = f"Seat-{i:03d}" # Generic fallback

                seat, created = Seat.objects.get_or_create(
                    name=seat_name,
                    # CHANGE THIS LINE: Use 'location' as the foreign key field name
                    location=section 
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  Created Seat: {seat.name} in {section.name}'))
                # else:
                #     self.stdout.write(self.style.WARNING(f'  Seat "{seat.name}" in "{section.name}" already exists.'))


        self.stdout.write(self.style.SUCCESS('Data population complete.'))