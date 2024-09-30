## restaurants/urls.py
## description: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app:
urlpatterns = [
    path(r'', views.main, name="home"), 
    path(r'main', views.main, name="main"), 
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation")
]