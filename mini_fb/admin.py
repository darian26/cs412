## Register the models with the Django Admin tool
# blog/admin.py
from django.contrib import admin
# Register your models here.
from .models import Profile, StatusMessage
admin.site.register(Profile)
admin.site.register(StatusMessage)