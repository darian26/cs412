'''
View file that renders the templates
'''

# view/views.py
# Define the views for the blog app:
#from django.shortcuts import render
from .models import *
from . forms import *
from django.urls import reverse ## NEW
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required

class EventsView(LoginRequiredMixin, ListView):
    """Create a subclass of ListView to display all events."""
    model = Event
    template_name = 'project/events.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch all events excluding the current user's events
        user = self.request.user
        userProfile = UserProfile.objects.get(user=user)
        user_events = Event.objects.filter(owner=userProfile)
        all_events = Event.objects.exclude(owner=userProfile)
        
        context['user_events'] = user_events
        context['all_events'] = all_events
        
        return context
    
    def get_login_url(self):
        return reverse('project_login')

class EventDetailView(LoginRequiredMixin, DetailView):
    '''Show the details for one event.'''
    model = Event
    template_name = 'project/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        context['current_event'] = event
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        event_registrations = user_profile.get_registered_events()
        registered_events = [registration.event for registration in event_registrations]
        context['registered_events'] = registered_events
        return context
    
    def get_login_url(self):
        return reverse('project_login')

class CreateEventRegistration(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        '''
        dispatch override
        '''
        profile = get_object_or_404(UserProfile, user=request.user)
        event = get_object_or_404(Event, pk=kwargs['pk'])
        profile.add_registration(event)
        return redirect('project_homepage')
    
    def get_login_url(self):
        return reverse('login')

class SignUpView(CreateView):
    '''a view to show/process the create comment form:
    on GET: sends back the form
    on POST: read the form data, create an instance of Comment; save to database; ??
    '''

    model = UserProfile 
    form_class = CreateUserProfileForm
    template_name = 'project/signup.html'
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successful profile creation'''
        return reverse('default_homepage') 

    def form_valid(self, form):
        '''This method executes after form submission if the form is valid'''

        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():  
            user = user_form.save()  
            
            profile = form.save(commit=False)  
            profile.user = user  
            profile.save()  
            
            login(self.request, user)

            return HttpResponseRedirect(self.get_success_url())
        else:
            context = self.get_context_data(form=form)
            context['user_form'] = user_form 
            return self.render_to_response(context)

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
class CreateEventView(CreateView, LoginRequiredMixin):
    '''a view to show/process the create comment form:
    on GET: sends back the form
    on POST: read the form data, create an instance of Comment; save to database; ??
    '''

    form_class = CreateEventForm
    template_name = "project/create_event_form.html"

    # what to do after form submission?
    def get_success_url(self) -> str:
        '''return the URL to redirect to after sucessful create'''
        print(self.object)
        return reverse("event_detail", kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        '''this method executes after form submission'''

        owner = get_object_or_404(UserProfile, user=self.request.user)
        form.instance.owner = owner
        form.save()

        return super().form_valid(form)
    

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        '''
        build the template context data --
        a dict of key-value pairs.'''

        # get the super class version of context data
        context = super().get_context_data(**kwargs)
        user = UserProfile.objects.get(user=self.request.user)

        # add the article to the context data
        context['user'] = user

        return context
    
    def get_login_url(self):
        return reverse('login')