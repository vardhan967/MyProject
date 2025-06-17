# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # Import BaseUserAdmin
from .models import User

class CustomUserAdmin(BaseUserAdmin): # Inherit from BaseUserAdmin
    # Define the fields to display for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password'), # Only prompt for username and password
        }),
    )
    # Define the fieldsets for changing an existing user
    # Exclude 'first_name', 'last_name', 'email' which you removed
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'is_staff') # What to show in the list view
    search_fields = ('username',) # How to search users


# Unregister the default UserAdmin if you had previously registered it without a custom class
# admin.site.unregister(User) # You might not need this line if you didn't unregister before

# Register your custom User model with your CustomUserAdmin
admin.site.register(User, CustomUserAdmin)