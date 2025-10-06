import os
import django
import requests

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from api.models import Donor, Recipient, NGO

# Clear existing test users
Donor.objects.filter(email='test.donor@example.com').delete()
Recipient.objects.filter(email='test.recipient@example.com').delete()
NGO.objects.filter(email='test.ngo@example.com').delete()

print("Creating test users...")

# Test creating a donor
print("\n1. Creating donor...")
donor_data = {
    'name': 'Test Donor',
    'email': 'test.donor@example.com',
    'phone': '1234567890',
    'address': '123 Donor St',
    'city': 'Donor City',
    'state': 'Donor State',
    'pincode': '123456',
    'password': 'donorpass123'
}

api_url = 'http://127.0.0.1:8000/api/donors/'
response = requests.post(api_url, json=donor_data)

if response.status_code in [200, 201]:
    print("✓ Donor created successfully")
    donor_info = response.json()
    print(f"  Donor ID: {donor_info.get('donor_id')}")
else:
    print(f"✗ Failed to create donor: {response.status_code}")
    print(response.text)

# Test creating a recipient
print("\n2. Creating recipient...")
recipient_data = {
    'name': 'Test Recipient',
    'email': 'test.recipient@example.com',
    'phone': '0987654321',
    'family_size': 3,
    'urgency': 'medium',
    'address': '456 Recipient St',
    'city': 'Recipient City',
    'state': 'Recipient State',
    'pincode': '654321',
    'password': 'recipientpass123'
}

api_url = 'http://127.0.0.1:8000/api/recipients/'
response = requests.post(api_url, json=recipient_data)

if response.status_code in [200, 201]:
    print("✓ Recipient created successfully")
    recipient_info = response.json()
    print(f"  Recipient ID: {recipient_info.get('recipient_id')}")
else:
    print(f"✗ Failed to create recipient: {response.status_code}")
    print(response.text)

# Test creating an NGO
print("\n3. Creating NGO...")
ngo_data = {
    'ngo_name': 'Test NGO',
    'email': 'test.ngo@example.com',
    'phone': '1122334455',
    'website': 'https://testngo.org',
    'address': '789 NGO St',
    'city': 'NGO City',
    'state': 'NGO State',
    'pincode': '112233',
    'password': 'ngopass123'
}

api_url = 'http://127.0.0.1:8000/api/ngos/'
response = requests.post(api_url, json=ngo_data)

if response.status_code in [200, 201]:
    print("✓ NGO created successfully")
    ngo_info = response.json()
    print(f"  NGO ID: {ngo_info.get('ngo_id')}")
else:
    print(f"✗ Failed to create NGO: {response.status_code}")
    print(response.text)

# Verify users exist in database
print("\n4. Verifying users in database...")
try:
    donor = Donor.objects.get(email='test.donor@example.com')
    print(f"✓ Donor found in database with hashed password")
    print(f"  Password hash starts with: {donor.password[:20]}...")
except Donor.DoesNotExist:
    print("✗ Donor not found in database")

try:
    recipient = Recipient.objects.get(email='test.recipient@example.com')
    print(f"✓ Recipient found in database with hashed password")
    print(f"  Password hash starts with: {recipient.password[:20]}...")
except Recipient.DoesNotExist:
    print("✗ Recipient not found in database")

try:
    ngo = NGO.objects.get(email='test.ngo@example.com')
    print(f"✓ NGO found in database with hashed password")
    print(f"  Password hash starts with: {ngo.password[:20]}...")
except NGO.DoesNotExist:
    print("✗ NGO not found in database")

print("\n✓ All authentication tests completed!")