import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import the Donor model
from api.models import Donor

# Delete all donors
donors = Donor.objects.all()
count = donors.count()
donors.delete()

print(f"Deleted {count} donors from the database.")