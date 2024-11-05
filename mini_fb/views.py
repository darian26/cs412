'''
View file that renders the templates
'''

# view/views.py
# Define the views for the blog app:
#from django.shortcuts import render
from .models import Profile, Image
from . forms import *
from django.urls import reverse ## NEW
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['current_profile'] = profile  
        return context

class CreateProfileView(CreateView):
    '''a view to show/process the create comment form:
    on GET: sends back the form
    on POST: read the form data, create an instance of Comment; save to database; ??
    '''

    model = Profile 
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successful profile creation'''
        return reverse('show_all_profiles') 

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
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

class CreateStatusMessageView(CreateView, LoginRequiredMixin):
    '''a view to show/process the create comment form:
    on GET: sends back the form
    on POST: read the form data, create an instance of Comment; save to database; ??
    '''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    # what to do after form submission?
    def get_success_url(self) -> str:
        '''return the URL to redirect to after sucessful create'''
        return reverse("profile", kwargs={'pk': self.object.profile.pk})
    
    def form_valid(self, form):
        '''this method executes after form submission'''

        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.profile = profile

        status_message = form.save()
        files = self.request.FILES.getlist('files')
        for f in files:
            # Create a new Image object for each file without the 'timestamp' field
            image = Image(
                image_file=f,  # Set the file in the ImageField
                status_message=status_message  # Link the image to the status message
            )
            image.save()

        return super().form_valid(form)
    

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        '''
        build the template context data --
        a dict of key-value pairs.'''

        # get the super class version of context data
        context = super().get_context_data(**kwargs)

        # find the article with the PK from the URL
        # self.kwargs['pk'] is finding the article PK from the URL
        profile = Profile.objects.get(user=self.request.user)

        # add the article to the context data
        context['profile'] = profile

        return context
    
    def get_login_url(self):
        return reverse('login')
    
class UpdateProfileView(UpdateView, LoginRequiredMixin):
    '''Class-based view for updating a user's profile.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        '''Override to redirect to the updated profile's detail page.'''
        return reverse('profile', kwargs={'pk': self.object.profile.pk})

    def get_context_data(self, **kwargs):
        '''Add additional context data to the template.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context
    
    def get_login_url(self):
        return reverse('login')
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    
class DeleteStatusMessageView(DeleteView, LoginRequiredMixin):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.profile.pk})
    
    def get_login_url(self):
        return reverse('login')

class UpdateStatusMessageView(UpdateView, LoginRequiredMixin):
    model = StatusMessage
    form_class = StatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.profile.pk})
    
    def get_login_url(self):
        return reverse('login')
    
class CreateFriendView(View, LoginRequiredMixin):
    ''' A view that allows a user to add a friend '''
    
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'post':
            profile = Profile.objects.get(user=request.user)
            other_profile = get_object_or_404(Profile, pk=kwargs['other_pk'])

            profile.add_friend(other_profile)
            return HttpResponseRedirect(self.get_success_url(profile.pk))
        
        return self.http_method_not_allowed(request, *args, **kwargs)
    
    def get_success_url(self, pk):
        ''' Return the URL to redirect to after adding a friend '''
        return reverse('profile', kwargs={'pk': pk})
    
    def get_login_url(self):
        return reverse('login')
    
class ShowFriendSuggestionsView(DetailView, LoginRequiredMixin):
    ''' A view to see friend suggestions '''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        print(profile)
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context
    
    def get_success_url(self):
        ''' Return the URL to redirect to after successful update '''
        return reverse('profile', kwargs={'pk': self.object.profile.pk})
    
    def get_login_url(self):
        return reverse('login')
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
class ShowNewsFeedView(DetailView, LoginRequiredMixin):
    ''' A view to see other status messages of friends '''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()
        return context

    def get_login_url(self):
        return reverse('login')
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)