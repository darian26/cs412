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


    def get_images(self):
        '''Return all of the images about this status message'''
        images = Image.objects.filter(status_message=self)
        return images

class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.status_message.text} uploaded at {self.uploaded_at}"