'''
This file is to store all the forms to be used in the view
'''

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image']

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['text']

class UpdateProfileForm(forms.ModelForm):
    '''Form to update the user's profile. Excludes first name and last name.'''
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image']

class StatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['text']
