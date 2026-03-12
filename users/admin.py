from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# The User model is already registered by Django's default auth app
# We can customize it here if needed in the future
