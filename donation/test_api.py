import requests
import json

# Test the donor API endpoint
url = 'http://127.0.0.1:8000/api/donors/'
data = {
    'name': 'Test Donor',
    'email': 'test@example.com',
    'phone': '1234567890',
    'address': '123 Test St',
    'city': 'Test City',
    'state': 'Test State',
    'pincode': '123456'
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Also test getting donors
    response = requests.get(url)
    print(f"\nGET Donors Status Code: {response.status_code}")
    print(f"GET Donors Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")