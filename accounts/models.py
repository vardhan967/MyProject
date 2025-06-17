# accounts/models.py

from django.contrib.auth.models import AbstractUser, UserManager # Import UserManager
from django.db import models

class CustomUserManager(UserManager): # Create a custom manager
    def _create_user(self, username, email, password, **extra_fields):
        """
        This method is overridden to remove the 'email' argument
        when creating a user, as our custom User model does not have an email field.
        """
        if not username:
            raise ValueError('The given username must be set')
        # The original _create_user method would use `self.normalize_email(email)`
        # but since we don't have an email field, we just set email to None
        email = None # Explicitly set email to None for compatibility if the original code tries to pass it.
        user = self.model(username=username, **extra_fields) # Do NOT pass 'email=email'
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, None, password, **extra_fields) # Pass None for email

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Pass None for email, as our model doesn't have an email field
        return self._create_user(username, None, password, **extra_fields)

class User(AbstractUser):
    # We'll use 'username' as 'roll_number' and make it the USERNAME_FIELD.
    # The default AbstractUser already has a username field.

    # Remove email and first/last name fields as not needed for simplicity
    # These fields are set to None to explicitly tell Django they don't exist
    email = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] # This ensures createsuperuser won't prompt for email

    objects = CustomUserManager() # <--- IMPORTANT: Use our custom manager

    def __str__(self):
        return self.username # Display roll number

    class Meta:
        verbose_name = 'Student Account'
        verbose_name_plural = 'Student Accounts'