'''
This file is to store all the forms to be used in the view
'''

from django import forms
from .models import *

class CreateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'age', 'city', 'profile_pfp']

class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date_time', 'capacity']

class UpdateEventForm(forms.ModelForm):
    '''Form to update the user's profile. Excludes first name and last name.'''
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date_time', 'capacity']

class UpdateUserProfileForm(forms.ModelForm):
    '''Form to update the user's profile. Excludes first name and last name.'''
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'age', 'city', 'profile_pfp']