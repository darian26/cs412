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
    
    def get_friends(self):
        '''
        Return all friends associated with this profile.
        '''
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        return [
            friend.profile2 if friend.profile1 == self else friend.profile1
            for friend in friends
        ]

    def add_friend(self, friend):
        '''
        Create a friend relation between self and another profile, if not already existing.
        '''
        if self != friend and not Friend.objects.filter(
            models.Q(profile1=self, profile2=friend) | models.Q(profile1=friend, profile2=self)
        ).exists():
            Friend.objects.create(profile1=self, profile2=friend)


    def get_friend_suggestions(self):
        '''
        Return a list of possible friends for the current profile
        '''
        all_profiles = Profile.objects.exclude(id=self.id)
        friends = Friend.objects.filter(
            models.Q(profile1=self) | models.Q(profile2=self)
        ).values_list('profile1', 'profile2')
        friend_ids = {profile1_id if profile1_id != self.id else profile2_id 
                    for profile1_id, profile2_id in friends}
        suggestions = all_profiles.exclude(id__in=friend_ids)
        
        return suggestions
    
    def get_news_feed(self):
        '''
        Return a QuerySet of StatusMessages for the profile and all their friends
        '''
        own_status = StatusMessage.objects.filter(profile=self)
        friends = self.get_friends()
        friend_status = StatusMessage.objects.filter(profile__in=friends)
        news_feed = own_status.union(friend_status).order_by('-timestamp')
        return news_feed
    
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
    
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name} " 