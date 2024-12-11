# File: models.py
# Author: Darian Cheung (darian26@bu.edu), 11/22/2024
# Description: this file models the data attributes of the events app
# Create your models here. 

from django.db import models 
from django.contrib.auth.models import User
from django.db.models import Case, When, Value, IntegerField

# User Model
class UserProfile(models.Model): 
    '''
    User model for the event's app
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    age = models.IntegerField()
    city = models.TextField()
    profile_pfp = models.URLField(blank=False) 
    joined_on = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self): 
        return f"{self.first_name} {self.last_name} joined on {self.joined_on} with pk of {self.pk}"
    
    def get_registration(self, event):
        return EventRegistration.objects.filter(user=self, event=event)
    
    def get_waitlist(self, event):
        return Waitlist.objects.filter(user=self, event=event)
    
    def remove_from_waitlist(self, event):
        Waitlist.objects.filter(user=self, event=event).delete()
        EventRegistration.objects.filter(user=self, event=event).delete()
    
    def add_registration(self, event):
        if len(EventRegistration.objects.filter(user=self, event=event, status = 'cancel')) > 0:
            existing_registration = EventRegistration.objects.get(user=self, event=event, status = 'cancel')
            existing_registration.status = 'going'
            existing_registration.save()
        else:
            EventRegistration.objects.create(
                user=self,
                event=event,
                status='going'
            )

    def add_waitlist(self, event):
        if len(Waitlist.objects.filter(user=self, event=event)) != 0:
            return 0
        else:
            if len(EventRegistration.objects.filter(user=self, event=event, status = 'cancel')) > 0:
                EventRegistration.objects.filter(user=self, event=event, status = 'cancel').delete()
                EventRegistration.objects.create(
                    user=self,
                    event=event,
                    status='waitlisted'
                )
                Waitlist.objects.create(
                    user=self,
                    event=event
                )
            else:
                Waitlist.objects.create(
                    user=self,
                    event=event
                )
                EventRegistration.objects.create(
                    user=self,
                    event=event,
                    status='waitlisted'
                )

    def get_registered_events(self):
        event_registrations = EventRegistration.objects.filter(user=self)
        registered_events = [registration.event for registration in event_registrations]
        return registered_events
    
    def get_event_registrations(self):
        event_registrations = EventRegistration.objects.filter(user=self).order_by('event__date_time')
        return event_registrations
    
    def get_hosted_events(self):
        return Event.objects.filter(owner=self)
    
    def cancel_registration(self, event):
        event_registration = EventRegistration.objects.get(user=self, event=event)
        event_registration.status = 'cancel'
        event_registration.save()
        going_count = len(EventRegistration.objects.filter(event=event, status='going'))

        if going_count < event.capacity:
            waitlist_to_going = Waitlist.objects.filter(event=event).order_by('added_on').first()
            if waitlist_to_going != None and waitlist_to_going.user != self:
                waitlist_registration = EventRegistration.objects.get(user=waitlist_to_going.user, event=event)
                waitlist_registration.status = 'going'
                waitlist_registration.save()
                waitlist_to_going.delete()
    
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
    
    def get_attendees(self):
        attendees = EventRegistration.objects.filter(event=self).annotate(
            status_priority=Case(
                When(status='going', then=Value(1)),
                When(status='waitlisted', then=Value(2)),
                When(status='cancel', then=Value(3)),
                output_field=IntegerField(),
            )
        ).order_by('status_priority')
        return attendees
    
    def calculate_capacity(self):
        """Calculate the number of 'going' registrations for this event."""
        going_count = EventRegistration.objects.filter(event=self, status='going').count()
        return going_count

# Event Registration Model
class EventRegistration(models.Model):
    '''
    EventRegistration model for the event's app
    '''
    STATUS_CHOICES = [
        ('going', 'Going'),
        ('cancel', 'Cancel'),
        ('waitlisted', 'Waitlisted')
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
