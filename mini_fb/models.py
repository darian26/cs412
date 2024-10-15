'''
Create a Model 
mini_fb/models.py
Define the data objects for our application
'''
from django.db import models
from django.urls import reverse ## NEW

class Profile(models.Model):
    '''Encapsulate the idea of an Profile by some user.'''
    # data attributes of a Article:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    profile_image = models.URLField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name} from {self.city}.'
    
    # new method:
    def get_status_message(self):
        '''Return all of the status message about this profile.'''
        status_message = StatusMessage.objects.filter(profile=self)
        status_message = status_message.order_by('-timestamp')
        return status_message
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})
    
class StatusMessage(models.Model):
    '''Encapsulate the idea of a status message on an Profile.'''
    
    # data attributes of a Comment:
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'{self.text}'
        