import os
import django
import requests

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import the Donation model
from api.models import Donation, Donor

print("=== Testing Donation System ===")

# First, let's make sure we have a donor
print("\n1. Checking for existing donors...")
donors = Donor.objects.all()
if donors.count() == 0:
    print("No donors found, creating a test donor...")
    donor = Donor.objects.create(
        name="Test Donor",
        email="test.donor@example.com",
        phone="1234567890",
        address="123 Test St",
        city="Test City",
        state="Test State",
        pincode="123456"
    )
    print(f"Created donor: {donor.name} (ID: {donor.donor_id})")
else:
    donor = donors.first()
    print(f"Using existing donor: {donor.name} (ID: {donor.donor_id})")

# Test the API directly
print("\n2. Testing donation API directly...")
api_url = 'http://127.0.0.1:8000/api/donations/'
donation_data = {
    'donor': donor.donor_id,
    'title': 'Test Donation',
    'description': 'This is a test donation',
    'category': 'Clothing',
    'quantity': 2,
    'status': 'pending'
}

response = requests.post(api_url, json=donation_data)
if response.status_code in [200, 201]:
    print("✓ API donation creation successful")
    donation_response = response.json()
    print(f"  Created donation ID: {donation_response.get('donation_id')}")
else:
    print("✗ API donation creation failed")
    print(f"  Status: {response.status_code}")
    print(f"  Error: {response.text}")

# Check database
print("\n3. Checking database...")
donations = Donation.objects.filter(donor=donor)
print(f"Total donations for donor: {donations.count()}")
for donation in donations:
    print(f"  - {donation.title} ({donation.category}): {donation.quantity} items [{donation.status}]")

print("\n=== Donation Test Complete ===")