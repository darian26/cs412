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
    path(r'create_event', views.CreateEventView.as_view(), name="create_event"),
    path(r'event/register_event/<int:pk>/', views.CreateEventRegistration.as_view(), name='event_register'),
    path(r'event/cancel_registration/<int:pk>/', views.CancelRegistration.as_view(), name='cancel_registration'),
    path(r'event/waitlist_event/<int:pk>/', views.JoinWaitlist.as_view(), name='event_waitlist'),
    path(r'event/remove_waitlist/<int:pk>/', views.RemoveWaitlist.as_view(), name='remove_waitlist'),
    path(r'registered_events', views.MyRegisteredEventsView.as_view(), name='registered_events'),
    path(r'event/register_event/<int:pk>/delete/', views.DeleteAttendee.as_view(), name='delete_attendee'),
    path(r'profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path(r'event/<int:pk>/update/', views.UpdateEventView.as_view(), name='update_event'),
    path(r'profile/<int:pk>', views.ShowProfileViewPage.as_view(), name="project_profile"),
    path(r'event/<int:pk>/delete/', views.DeleteEvent.as_view(), name='delete_event'),
]