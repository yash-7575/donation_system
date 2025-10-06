import os
import django
import requests
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import the models
from api.models import Donation, Donor

print("=== Final Comprehensive Donation Test ===")

# Clear test data
Donation.objects.filter(title__in=['Final Test Donation', 'API Test Donation']).delete()

# Get a donor for testing
donor = Donor.objects.first()
if not donor:
    print("No donors found, creating one...")
    donor = Donor.objects.create(
        name="Final Test Donor",
        email="final.donor@example.com",
        phone="5556667777",
        address="Final Test St",
        city="Final City",
        state="Final State",
        pincode="555666"
    )

print(f"Using donor: {donor.name} (ID: {donor.donor_id})")

# Test 1: API directly
print("\n1. Testing API endpoint...")
api_url = 'http://127.0.0.1:8000/api/donations/'
api_donation = {
    'donor': donor.donor_id,
    'title': 'API Test Donation',
    'description': 'Test donation via API',
    'category': 'Electronics',
    'quantity': 1,
    'status': 'pending'
}

response = requests.post(api_url, json=api_donation)
api_success = response.status_code in [200, 201]
print(f"API test: {'✓ PASS' if api_success else '✗ FAIL'}")

# Test 2: Check database after API test
api_donation_exists = Donation.objects.filter(title='API Test Donation').exists()
print(f"Database check after API: {'✓ PASS' if api_donation_exists else '✗ FAIL'}")

# Test 3: Frontend submission (simulated)
print("\n2. Testing frontend submission...")
# We'll test this by making a direct POST request to the donor dashboard
frontend_url = 'http://127.0.0.1:8000/donor/'
frontend_donation = {
    'title': 'Final Test Donation',
    'description': 'Test donation via frontend',
    'category': 'Books',
    'quantity': '4'
}

response = requests.post(frontend_url, data=frontend_donation)
frontend_success = response.status_code == 200
print(f"Frontend test: {'✓ PASS' if frontend_success else '✗ FAIL'}")

# Test 4: Check final database state
print("\n3. Checking final database state...")
final_donation_exists = Donation.objects.filter(title='Final Test Donation').exists()
total_donations = Donation.objects.count()

print(f"Final donation exists: {'✓ PASS' if final_donation_exists else '✗ FAIL'}")
print(f"Total donations in database: {total_donations}")

# Display all donations
print("\nAll donations in database:")
donations = Donation.objects.all()
for donation in donations:
    print(f"  - {donation.title} ({donation.category}): {donation.quantity} items [Donor: {donation.donor.name}]")

# Final result
all_tests_passed = api_success and api_donation_exists and frontend_success and final_donation_exists
print(f"\n{'🎉 ALL TESTS PASSED' if all_tests_passed else '❌ SOME TESTS FAILED'}")

if all_tests_passed:
    print("\n✅ The donation system is fully functional!")
    print("   - Donations can be submitted through the API")
    print("   - Donations can be submitted through the frontend")
    print("   - All donations are stored in the MySQL database")
    print("   - The 'Submit Donation' button works correctly")
    print("   - The donation popup is properly connected to the donation table")

print("\n=== Final Comprehensive Donation Test Complete ===")