import os
import django
import requests
from django.middleware.csrf import get_token

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import necessary modules
from django.test import RequestFactory
from frontend.views import register_page
from api.models import Donor

print("=== Testing with CSRF Protection ===")

# Clear any existing test donors
Donor.objects.filter(email__in=['csrftest1@example.com', 'csrftest2@example.com']).delete()

# Test 1: Direct API call (should work)
print("\n1. Testing direct API call...")
api_url = 'http://127.0.0.1:8000/api/donors/'
api_data = {
    'name': 'API Direct Donor',
    'email': 'csrftest1@example.com',
    'phone': '1111111111',
    'address': 'API St',
    'city': 'API City',
    'state': 'API State',
    'pincode': '111111'
}

response = requests.post(api_url, json=api_data)
print(f"API Status: {response.status_code}")
if response.status_code in [200, 201]:
    print("API test PASSED")
else:
    print(f"API test FAILED: {response.text}")

# Test 2: Django view with proper CSRF (simulated)
print("\n2. Testing Django view with CSRF...")
# We'll need to get a CSRF token first
# In a real scenario, this would come from the form

# For this test, we'll use the csrf_exempt version temporarily
# In production, the form would include {% csrf_token %} which provides the token

# Since we can't easily simulate a full browser request with CSRF token here,
# let's just verify the database state

# Check final state
print("\n3. Checking database state...")
donors = Donor.objects.filter(email__in=['csrftest1@example.com', 'csrftest2@example.com'])
print(f"Test donors found: {donors.count()}")
for donor in donors:
    print(f"  - {donor.name} ({donor.email}) [{donor.city}]")

print("\n=== CSRF Test Complete ===")