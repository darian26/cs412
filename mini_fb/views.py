'''
View file that renders the templates
'''

# view/views.py
# Define the views for the blog app:
#from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView
class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog profiles.'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ShowProfileViewPage(DetailView):
    '''Show the details for one profile.'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'