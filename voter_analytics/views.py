'''
Views for the voter_analytics app
'''

from django.views.generic import ListView, DetailView
from .models import Voter  
from django.db.models.query import QuerySet
from django.db.models import Q, Count  
from datetime import date  
import plotly.express as px
from plotly.offline import plot

class VoterListView(ListView):
    '''View to display list of voters with filtering options.'''

    template_name = 'voter_analytics/voter_list.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100  

    def get_queryset(self) -> QuerySet:
        '''Return a filtered queryset of Voters based on search parameters.'''

        queryset = super().get_queryset()

        party_affiliation = self.request.GET.get('party_affiliation')
        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)

        min_dob = self.request.GET.get('min_dob')
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=date(int(min_dob), 1, 1))

        max_dob = self.request.GET.get('max_dob')
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=date(int(max_dob), 12, 31))

        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))

        election_fields = ['v20_state', 'v21_town', 'v21_primary', 'v22_general', 'v23_town']
        for field in election_fields:
            if self.request.GET.get(field) == 'true':
                if field == 'v20_state':
                    queryset = queryset.filter(v20_state=True)
                elif field == 'v21_town':
                    queryset = queryset.filter(v21_town=True)
                elif field == 'v21_primary':
                    queryset = queryset.filter(v21_primary=True)
                elif field == 'v22_general':
                    queryset = queryset.filter(v22_general=True)
                elif field == 'v23_town':
                    queryset = queryset.filter(v23_town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = range(1913, 2006)
        context['voter_scores'] = range(1, 6)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        return context

class VoterDetailView(DetailView): 
    ''' A view to show a page for a single Voter record '''

    model = Voter 
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterGraphsView(ListView): 
    ''' A view to show the graphing data for voters '''

    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self) -> QuerySet:
        '''Return a filtered queryset of Voters based on search parameters.'''

        queryset = super().get_queryset()

        party_affiliation = self.request.GET.get('party_affiliation')
        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)

        min_dob = self.request.GET.get('min_dob')
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=date(int(min_dob), 1, 1))

        max_dob = self.request.GET.get('max_dob')
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=date(int(max_dob), 12, 31))

        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))

        election_fields = ['v20_state', 'v21_town', 'v21_primary', 'v22_general', 'v23_town']
        for field in election_fields:
            if self.request.GET.get(field) == 'true':
                if field == 'v20_state':
                    queryset = queryset.filter(v20_state=True)
                elif field == 'v21_town':
                    queryset = queryset.filter(v21_town=True)
                elif field == 'v21_primary':
                    queryset = queryset.filter(v21_primary=True)
                elif field == 'v22_general':
                    queryset = queryset.filter(v22_general=True)
                elif field == 'v23_town':
                    queryset = queryset.filter(v23_town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        birth_years = queryset.values_list('date_of_birth', flat=True)
        birth_years = [dob.year for dob in birth_years]
        fig1 = px.histogram(x=birth_years, nbins=20, labels={'x': 'Year of Birth'}, title="Distribution of Voters by Year of Birth")
        context['birth_year_histogram'] = plot(fig1, output_type='div')

        party_counts = queryset.values('party_affiliation').annotate(count=Count('party_affiliation'))
        fig2 = px.pie(party_counts, names='party_affiliation', values='count', title="Voters by Party Affiliation", width=600, height=600)
        context['party_affiliation_pie'] = plot(fig2, output_type='div')

        elections = ['v20_state', 'v21_town', 'v21_primary', 'v22_general', 'v23_town']
        participation_counts = {election: queryset.filter(**{election: True}).count() for election in elections}
        fig3 = px.bar(x=list(participation_counts.keys()), y=list(participation_counts.values()), labels={'x': 'Election', 'y': 'Count'}, title="Voters by Election Participation")
        context['election_participation_histogram'] = plot(fig3, output_type='div')

        context['years'] = range(1913, 2006)
        context['voter_scores'] = range(1, 6)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        return context