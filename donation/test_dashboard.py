import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import necessary modules
from django.test import RequestFactory
from frontend.views import donor_dashboard

print("=== Testing Enhanced Donor Dashboard ===")

# Test that the dashboard renders correctly
print("\n1. Testing dashboard rendering...")

factory = RequestFactory()
request = factory.get('/donor/')

# Call the view function
response = donor_dashboard(request)

print(f"Response status code: {response.status_code}")
print(f"Response type: {type(response)}")

if response.status_code == 200:
    print("✓ Dashboard renders successfully")
else:
    print("✗ Dashboard rendering failed")

# Check that the response contains expected elements
content = response.content.decode('utf-8')

expected_elements = [
    'Donate New Item',
    'My Donations',
    'Total Donations',
    'Item Title',
    'Description',
    'Category',
    'Quantity'
]

print("\n2. Checking for expected elements...")
all_found = True
for element in expected_elements:
    if element in content:
        print(f"✓ Found: {element}")
    else:
        print(f"✗ Missing: {element}")
        all_found = False

if all_found:
    print("\n🎉 SUCCESS: Enhanced donor dashboard is properly structured!")
else:
    print("\n❌ FAILURE: Some expected elements are missing.")

print("\n=== Dashboard Test Complete ===")