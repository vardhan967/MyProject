# accounts/management/commands/populate_students.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Populates the database with student user accounts (22A91A6101 to 22A91A6199).'

    def handle(self, *args, **options):
        User = get_user_model()
        password = 'Aditya@123'

        self.stdout.write(self.style.SUCCESS('Starting student account population...'))

        for i in range(1, 100):
            username_suffix = f"{i:02d}"
            username = f"22A91A61{username_suffix}"
            # Removed the email creation line: email = f"{username}@example.com"

            try:
                # Removed 'email': email from defaults
                user, created = User.objects.get_or_create(username=username) # No defaults needed if only username

                if created:
                    user.set_password(password)
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))
                else:
                    self.stdout.write(self.style.WARNING(f'User "{username}" already exists. Skipping.'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating user {username}: {e}'))

        self.stdout.write(self.style.SUCCESS('Student account population complete.'))