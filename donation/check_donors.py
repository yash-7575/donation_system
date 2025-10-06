import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import the Donor model
from api.models import Donor

# Fetch and display all donors
donors = Donor.objects.all()
print(f'Total donors: {donors.count()}')
for donor in donors:
    print(f'Donor: {donor.name}, Email: {donor.email}, City: {donor.city}')