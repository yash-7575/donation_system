import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import necessary modules
from django.test import RequestFactory
from frontend.views import register_page
from api.models import Donor

# Create a request factory
factory = RequestFactory()

# Create a POST request simulating form submission
request = factory.post('/register/', {
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'phone': '9876543210',
    'address': '456 Main St',
    'city': 'Sample City',
    'state': 'Sample State',
    'pincode': '654321',
    'role': 'donor'
})

# Call the view function
response = register_page(request)

print(f"Response status code: {response.status_code}")
print(f"Response type: {type(response)}")

# Check if donor was created
try:
    donor = Donor.objects.get(email='john.doe@example.com')
    print(f"Successfully created donor: {donor.name}")
except Donor.DoesNotExist:
    print("Donor was not created in the database")
    # List all donors to see what's in the database
    donors = Donor.objects.all()
    print(f"Total donors in database: {donors.count()}")
    for d in donors:
        print(f"  - {d.name} ({d.email})")