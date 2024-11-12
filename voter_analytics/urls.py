'''
url patterns for the voter_analytics app
'''

from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
    path('graphs/', VoterGraphsView.as_view(), name='graphs'), 
]