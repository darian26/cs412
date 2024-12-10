## Register the models with the Django Admin tool
# blog/admin.py
from django.contrib import admin
# Register your models here.
from .models import *
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(Location)
admin.site.register(Waitlist)