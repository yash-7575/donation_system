import os
import django
import requests
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Test the API directly first
print("Testing API directly...")
api_url = 'http://127.0.0.1:8000/api/donors/'
donor_data = {
    'name': 'Debug Donor',
    'email': 'debug@example.com',
    'phone': '1111111111',
    'address': 'Debug St',
    'city': 'Debug City',
    'state': 'Debug State',
    'pincode': '111111'
}

try:
    response = requests.post(api_url, json=donor_data)
    print(f"API Status Code: {response.status_code}")
    print(f"API Response: {response.text}")
    
    # Also test getting donors
    response = requests.get(api_url)
    print(f"\nGET Donors Status Code: {response.status_code}")
    print(f"GET Donors Response: {response.text}")
except Exception as e:
    print(f"Error testing API: {e}")

# Now test the database directly
print("\nChecking database directly...")
from api.models import Donor

# List all donors
donors = Donor.objects.all()
print(f"Total donors in database: {donors.count()}")
for donor in donors:
    print(f"  - {donor.name} ({donor.email})")