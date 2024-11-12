'''
Create a Model 
mini_fb/models.py
Define the data objects for our application
'''
import csv
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Voter(models.Model):
    '''
    Store/represent the data from one registered voter from Newton.
    '''
    voter_id = models.CharField(max_length=20)
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apt_number = models.TextField()
    zip_code = models.IntegerField()
    date_of_birth = models.DateField()
    day_of_reg = models.DateField()
    party_affiliation = models.CharField(max_length=1)
    precinct_number = models.CharField(max_length=1)
    v20_state = models.BooleanField()
    v21_town = models.BooleanField()
    v21_primary = models.BooleanField()
    v22_general = models.BooleanField()
    v23_town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} {self.zip_code}'
    
def load_data(): 
    '''
    Function to load data records from CSV file into Django model instances.
    '''
    
    filename = '/Users/dari/cs412/newton_voters.csv'
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            voter = Voter(
                voter_id= row[0],
                last_name=row[1],
                first_name=row[2],
                street_number=int(row[3]),
                street_name=row[4],
                apt_number=row[5],
                zip_code=int(row[6]),
                date_of_birth=row[7],
                day_of_reg=row[8],
                party_affiliation=row[9],
                precinct_number=row[10],
                v20_state=row[11].strip().lower() == 'true',
                v21_town=row[12].strip().lower() == 'true',
                v21_primary=row[13].strip().lower() == 'true',
                v22_general=row[14].strip().lower() == 'true',
                v23_town=row[15].strip().lower() == 'true',
                voter_score=int(row[16])
            )
            voter.save()
            print(f'Created voter: {voter}')