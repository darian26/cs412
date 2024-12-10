# File: models.py
# Author: Darian Cheung (darian26@bu.edu), 11/22/2024
# Description: this file models the data attributes of the events app
# Create your models here. 

from django.db import models 
from django.contrib.auth.models import User

# User Model
class UserProfile(models.Model): 
    '''
    User model for the event's app
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.TextField() 
    last_name = models.TextField() 
    email = models.EmailField()
    profile_pfp = models.URLField(blank=False) 
    joined_on = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self): 
        return f"{self.first_name} {self.last_name} joined on {self.joined_on}"
    
    def add_registration(self, event):
        EventRegistration.objects.create(
            user=self,
            event=event,
            status='going'
        )

    def get_registered_events(self):
        return EventRegistration.objects.filter(user=self)
    
# Event Model
class Event(models.Model):
    title = models.TextField()
    description = models.TextField()
    location = models.TextField()
    date_time = models.DateTimeField()
    capacity = models.IntegerField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_all_events_excluding_user(self, user):
        """Fetch all events except those created by the given user."""
        return Event.objects.exclude(owner=user)

    def get_user_events(self, user):
        """Fetch events created by the given user."""
        return Event.objects.filter(owner=user)

# Event Registration Model
class EventRegistration(models.Model):
    '''
    EventRegistration model for the event's app
    '''
    STATUS_CHOICES = [
        ('going', 'Going'),
        ('cancel', 'Cancel'),
        ('waitlisted', 'Waitlisted'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.user.first_name} - {self.event.title} ({self.status})"


# Waitlist Model
class Waitlist(models.Model):
    '''
    Waitlist model for the event's app
    '''
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    added_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.event.title} (Waitlisted)"

# Location Model
class Location(models.Model):
    '''
    Location model for the event's app
    '''
    location_name = models.TextField()
    rating = models.IntegerField()
    comments = models.TextField(null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='location_event')

    def __str__(self):
        return f"{self.location_name} - {self.rating}/5"
