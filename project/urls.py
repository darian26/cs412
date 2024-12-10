## pages/urls.py
## description: the app-specific URLS for the hw application

from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

# create a list of URLs for this app:
urlpatterns = [
    path(r'', auth_views.LoginView.as_view(template_name="project/login.html"), name='default_login'),
    path('login/', auth_views.LoginView.as_view(template_name="project/login.html"), name='project_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logout.html'), name="project_logout"),
    path(r'signup', views.SignUpView.as_view(), name="project_signup"),
    path(r'home', views.EventsView.as_view(), name="project_homepage"),
    path(r'event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path(r'event/create_event', views.CreateEventView.as_view(), name="create_event"),
    path(r'event/register_event/<int:pk>/', views.CreateEventRegistration.as_view(), name='event_register'),
]