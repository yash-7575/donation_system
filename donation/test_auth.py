import os
import django
import requests

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from api.models import Donor

# Clear existing test donors
Donor.objects.filter(email='test.auth@example.com').delete()

# Test creating a new donor with password
print("Creating test donor...")
donor_data = {
    'name': 'Auth Test Donor',
    'email': 'test.auth@example.com',
    'phone': '1234567890',
    'address': '123 Test St',
    'city': 'Test City',
    'state': 'Test State',
    'pincode': '123456',
    'password': 'testpassword123'
}

# Test API endpoint
api_url = 'http://127.0.0.1:8000/api/donors/'
response = requests.post(api_url, json=donor_data)

if response.status_code in [200, 201]:
    print("✓ Donor created successfully via API")
    donor_info = response.json()
    print(f"  Donor ID: {donor_info.get('donor_id')}")
    print(f"  Name: {donor_info.get('name')}")
    print(f"  Email: {donor_info.get('email')}")
    print("  Password field is excluded from response")
else:
    print(f"✗ Failed to create donor: {response.status_code}")
    print(response.text)

# Verify donor exists in database
try:
    donor = Donor.objects.get(email='test.auth@example.com')
    print(f"✓ Donor found in database with hashed password")
    print(f"  Password hash starts with: {donor.password[:20]}...")
except Donor.DoesNotExist:
    print("✗ Donor not found in database")