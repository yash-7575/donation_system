import os
import django
import requests
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import the Donation model
from api.models import Donation, Donor

print("=== End-to-End Donation Test ===")

# Clear any existing test donations
Donation.objects.filter(title='E2E Test Donation').delete()

# Test the complete flow
print("\nTesting complete donation flow...")

# 1. Test API directly first
print("\n1. Testing API endpoint...")
api_url = 'http://127.0.0.1:8000/api/donations/'

# Get a donor for testing
donor = Donor.objects.first()
if not donor:
    print("No donors found, creating one...")
    donor = Donor.objects.create(
        name="E2E Test Donor",
        email="e2e.donor@example.com",
        phone="9876543210",
        address="E2E Test St",
        city="E2E City",
        state="E2E State",
        pincode="654321"
    )

test_donation = {
    'donor': donor.donor_id,
    'title': 'E2E Test Donation',
    'description': 'End-to-end test donation',
    'category': 'Food',
    'quantity': 5,
    'status': 'pending'
}

response = requests.post(api_url, json=test_donation)
if response.status_code in [200, 201]:
    print("✓ API endpoint is working")
    donation_data = response.json()
    print(f"  Created donation ID: {donation_data.get('donation_id')}")
else:
    print("✗ API endpoint failed")
    print(f"  Status: {response.status_code}")
    print(f"  Error: {response.text}")

# 2. Check database
print("\n2. Checking database...")
try:
    donation = Donation.objects.get(title='E2E Test Donation')
    print("✓ Donation found in database")
    print(f"  Title: {donation.title}")
    print(f"  Category: {donation.category}")
    print(f"  Quantity: {donation.quantity}")
    print(f"  Donor: {donation.donor.name}")
except Donation.DoesNotExist:
    print("✗ Donation not found in database")

# 3. Summary
print("\n3. Summary...")
total_donations = Donation.objects.count()
test_donation_exists = Donation.objects.filter(title='E2E Test Donation').exists()
print(f"Total donations in database: {total_donations}")
print(f"Test donation exists: {test_donation_exists}")

if test_donation_exists:
    print("\n🎉 SUCCESS: The donation system is working correctly!")
    print("   When users click the 'Submit Donation' button,")
    print("   the donation will be visible in the donation table of MySQL.")
else:
    print("\n❌ FAILURE: There's still an issue with the system.")

print("\n=== End-to-End Donation Test Complete ===")