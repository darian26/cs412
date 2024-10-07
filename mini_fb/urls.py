'''
mini_fb/urls.py
description: the app-specific URLS for the mini_db application
'''
from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app:
urlpatterns = [
    # path(url, view, name)
    path(r'', views.ShowAllView.as_view(), name="show_all"), 
   
]