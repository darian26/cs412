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
        
        # Fetch all users for the dropdown
        all_users = UserProfile.objects.all()
        
        # Get the current user
        user = self.request.user
        userProfile = UserProfile.objects.get(user=user)
        
        # Default to showing all events excluding current user's events
        all_events = Event.objects.exclude(owner=userProfile)
        user_events = Event.objects.filter(owner=userProfile)
        
        # Check if a specific user is selected for filtering
        selected_user_id = self.request.GET.get('user_filter')
        if selected_user_id:
            try:
                selected_user = UserProfile.objects.get(pk=selected_user_id)
                all_events = Event.objects.filter(owner=selected_user)
            except UserProfile.DoesNotExist:
                pass
        
        context['user_events'] = user_events
        context['all_events'] = all_events
        context['all_users'] = all_users
        context['selected_user_id'] = int(selected_user_id) if selected_user_id else None
        
        return context
    
    def get_login_url(self):
        return reverse('project_login')
    
class MyRegisteredEventsView(LoginRequiredMixin, ListView):
    """Create a subclass of ListView to display all events."""
    model = EventRegistration
    template_name = 'project/registered_events.html'
    context_object_name = 'event_registrations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch all events excluding the current user's events
        user = self.request.user
        userProfile = UserProfile.objects.get(user=user)
        user_events = userProfile.get_event_registrations()
        
        context['user_events'] = user_events        
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
        registered_events = user_profile.get_registered_events()
        context['registered_events'] = registered_events
        user_registration_for_event = user_profile.get_registration(event)
        user_waitlist_for_event = user_profile.get_waitlist(event)
        if len(user_registration_for_event) != 0:
            context['event_registration'] = user_registration_for_event[0]
            context['er_pk'] = user_registration_for_event[0].pk
        else:
            context['event_registration'] = None
            context['er_pk'] = None
        
        if len(user_waitlist_for_event) != 0:
            context['waitlist_pk'] = user_waitlist_for_event[0].pk
        else:
            context['waitlist_pk'] = None

        going = event.calculate_capacity()
        context['capacity'] = going
        context['full'] = (going == event.capacity)
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
    
class JoinWaitlist(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        '''
        dispatch override
        '''
        profile = get_object_or_404(UserProfile, user=request.user)
        event = get_object_or_404(Event, pk=kwargs['pk'])
        profile.add_waitlist(event)
        return redirect('project_homepage')
    
    def get_login_url(self):
        return reverse('login')
    
class DeleteAttendee(DeleteView, LoginRequiredMixin):
    model = EventRegistration
    template_name = 'project/delete_attendee.html'
    context_object_name = 'eventRegistration'

    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.event.pk})
    
    def get_login_url(self):
        return reverse('project_login')
    
    def form_valid(self, form):
        # Get the event associated with this registration
        event = self.object.event
        
        # Check if there are waitlisted users for this event
        waitlist_entries = Waitlist.objects.filter(event=event).order_by('added_on')
        print(waitlist_entries)
        print((event.calculate_capacity() - 1))
        print(event.capacity)
        if waitlist_entries.exists() and event.calculate_capacity() - 1 < event.capacity :
            # Get the first waitlist entry
            waitlist_to_going = waitlist_entries[0]
            
            # Update the corresponding event registration to 'going'
            waitlist_registration = EventRegistration.objects.get(
                user=waitlist_to_going.user, 
                event=event
            )
            waitlist_registration.status = 'going'
            waitlist_registration.save()
            
            # Remove the waitlist entry
            waitlist_to_going.delete()
            self.object.delete()
        return redirect('project_homepage')

class CancelRegistration(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        '''
        dispatch override
        '''
        profile = get_object_or_404(UserProfile, user=request.user)
        event = get_object_or_404(Event, pk=kwargs['pk'])
        profile.cancel_registration(event)
        return redirect('project_homepage')
    
    def get_login_url(self):
        return reverse('login')   

class RemoveWaitlist(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        '''
        dispatch override
        '''
        profile = get_object_or_404(UserProfile, user=request.user)
        event = get_object_or_404(Event, pk=kwargs['pk'])
        profile.remove_from_waitlist(event)
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
        return reverse('project_homepage') 

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
        if self.request.user != None: 
            user = UserProfile.objects.get(user=self.request.user)
            context['user_profile'] = user
        else:
            context['user_profile'] = None

        # add the article to the context data

        return context
    
    def get_login_url(self):
        return reverse('project_login')

class UpdateProfileView(UpdateView, LoginRequiredMixin):
    '''Class-based view for updating a user's profile.'''

    model = UserProfile
    form_class = UpdateUserProfileForm
    template_name = 'project/update_profile_form.html'

    def get_success_url(self):
        '''Override to redirect to the updated profile's detail page.'''
        profile = self.get_object()
        return reverse('project_profile', kwargs={'pk': profile.pk})

    def get_object(self):
        '''
        returns the object
        '''
        return get_object_or_404(UserProfile, user=self.request.user)
    
    def get_login_url(self):
        return reverse('project_login')
    
class ShowProfileViewPage(DetailView):
    '''Show the details for one profile.'''
    model = UserProfile
    template_name = 'project/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['current_profile'] = profile
        return context
    
class DeleteEvent(DeleteView, LoginRequiredMixin):
    model = Event
    template_name = 'project/delete_event.html'
    context_object_name = 'event'

    def get_success_url(self):
        return reverse('project_homepage')
    
    def get_login_url(self):
        return reverse('login')

class UpdateEventView(UpdateView, LoginRequiredMixin):
    '''Class-based view for updating a user's profile.'''

    model = Event
    form_class = UpdateEventForm
    template_name = 'project/update_event_form.html'

    def get_success_url(self):
        '''Override to redirect to the updated profile's detail page.'''
        return reverse('event_detail', kwargs={'pk': self.object.pk})
    
    def get_login_url(self):
        return reverse('project_login')