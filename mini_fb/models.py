'''
Create a Model 
mini_fb/models.py
Define the data objects for our application
'''
from django.db import models
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