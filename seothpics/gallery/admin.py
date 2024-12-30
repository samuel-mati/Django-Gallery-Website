# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import CustomUserCreationForm
# Register the custom user model in the admin interface
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm  # Form for adding new users
    
    model = CustomUser

    # List the fields you want to display in the admin interface
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    search_fields = ['username', 'email']
    ordering = ['username']
    
    # Define fieldsets to organize the form fields
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Add the fields to be shown when adding a user
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Image)
admin.site.register(Category)
admin.site.register(ImageDownload)
admin.site.register(ImageLike)