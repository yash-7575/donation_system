import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import necessary modules
import logging
from django.test import RequestFactory
from django.http import HttpRequest
from frontend.views import register_page
from api.models import Donor

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO)

# Clear any existing donors for a clean test
Donor.objects.filter(email='test.request@example.com').delete()

# Create a POST request simulating form submission using RequestFactory
factory = RequestFactory()
request = factory.post('/register/', {
    'name': 'Request Test Donor',
    'email': 'test.request@example.com',
    'phone': '5555555555',
    'address': 'Request Test St',
    'city': 'Request City',
    'state': 'Request State',
    'pincode': '55555',
    'role': 'donor'
})

# Add host information to simulate a real request
request.META['HTTP_HOST'] = '127.0.0.1:8000'

print("Testing Django view with simulated request...")

# Call the view function
response = register_page(request)

print(f"Response status code: {response.status_code}")
print(f"Response type: {type(response)}")

if hasattr(response, 'url'):
    print(f"Response URL: {response.url}")

# Check if donor was created
try:
    donor = Donor.objects.get(email='test.request@example.com')
    print(f"SUCCESS: Donor created - {donor.name}")
except Donor.DoesNotExist:
    print("ERROR: Donor was not created in the database")
    # List all donors to see what's in the database
    donors = Donor.objects.all()
    print(f"Total donors in database: {donors.count()}")
    for d in donors:
        print(f"  - {d.name} ({d.email})")