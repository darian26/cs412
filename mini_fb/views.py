from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# view/views.py
# Define the views for the blog app:
#from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView
class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog profiles.'''
    model = Profile # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_all.html'
    context_object_name = 'profiles' # how to find the data in the template file