import os
import django
import requests
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import necessary modules
from django.test import RequestFactory
from frontend.views import donor_dashboard
from api.models import Donation, Donor

print("=== Frontend Donation Test ===")

# Clear any existing test donations
Donation.objects.filter(title='Frontend Test Donation').delete()

# Get a donor for testing
donor = Donor.objects.first()
if not donor:
    print("No donors found, creating one...")
    donor = Donor.objects.create(
        name="Frontend Test Donor",
        email="frontend.donor@example.com",
        phone="1112223333",
        address="Frontend Test St",
        city="Frontend City",
        state="Frontend State",
        pincode="111222"
    )

# Test the Django view with a POST request
print("\nTesting frontend donation submission...")

factory = RequestFactory()
request = factory.post('/donor/', {
    'title': 'Frontend Test Donation',
    'description': 'Frontend test donation',
    'category': 'Clothing',
    'quantity': '3'
})

# Call the view function
response = donor_dashboard(request)

print(f"Response status code: {response.status_code}")
print(f"Response type: {type(response)}")

if hasattr(response, 'content'):
    try:
        content = json.loads(response.content)
        print(f"Response content: {content}")
        if content.get('success'):
            print("✓ Frontend donation submission successful")
        else:
            print(f"✗ Frontend donation submission failed: {content.get('error')}")
    except:
        print(f"Response content (not JSON): {response.content}")

# Check database
print("\nChecking database...")
try:
    donation = Donation.objects.get(title='Frontend Test Donation')
    print("✓ Donation found in database")
    print(f"  Title: {donation.title}")
    print(f"  Category: {donation.category}")
    print(f"  Quantity: {donation.quantity}")
    print(f"  Donor: {donation.donor.name}")
except Donation.DoesNotExist:
    print("✗ Donation not found in database")

print("\n=== Frontend Donation Test Complete ===")