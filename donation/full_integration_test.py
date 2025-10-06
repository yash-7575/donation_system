import os
import django
import requests
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import the Donor model
from api.models import Donor

print("=== Full Integration Test ===")

# 1. Check initial state
print("\n1. Checking initial database state...")
initial_count = Donor.objects.count()
print(f"Initial donor count: {initial_count}")

# 2. Test API directly
print("\n2. Testing API directly...")
api_url = 'http://127.0.0.1:8000/api/donors/'
donor_data = {
    'name': 'API Test Donor',
    'email': 'api.test@example.com',
    'phone': '1234509876',
    'address': 'API Test St',
    'city': 'API City',
    'state': 'API State',
    'pincode': '102938'
}

response = requests.post(api_url, json=donor_data)
print(f"API POST Status: {response.status_code}")
if response.status_code in [200, 201]:
    print("API test PASSED")
    api_donor = response.json()
    print(f"Created donor ID: {api_donor.get('donor_id')}")
else:
    print(f"API test FAILED: {response.text}")

# 3. Check database after API test
print("\n3. Checking database after API test...")
api_test_count = Donor.objects.count()
print(f"Donor count after API test: {api_test_count}")

# 4. Test Django view
print("\n4. Testing Django view...")
# We'll simulate this by making a direct POST request to the register endpoint
register_url = 'http://127.0.0.1:8000/register/'
view_donor_data = {
    'name': 'View Test Donor',
    'email': 'view.test@example.com',
    'phone': '6789054321',
    'address': 'View Test St',
    'city': 'View City',
    'state': 'View State',
    'pincode': '987654',
    'role': 'donor'
}

# Note: This test won't work perfectly without CSRF token, but let's see what happens
try:
    response = requests.post(register_url, data=view_donor_data)
    print(f"View POST Status: {response.status_code}")
    print(f"View Response URL: {response.url if hasattr(response, 'url') else 'N/A'}")
except Exception as e:
    print(f"View test error: {e}")

# 5. Check final database state
print("\n5. Checking final database state...")
final_count = Donor.objects.count()
print(f"Final donor count: {final_count}")

donors = Donor.objects.all()
print(f"\nAll donors in database ({donors.count()}):")
for donor in donors:
    print(f"  - {donor.name} ({donor.email}) [{donor.city}]")

print("\n=== Test Complete ===")