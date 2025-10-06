import os
import django
import requests

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.test import RequestFactory
from frontend.views import login_page

# Test login functionality
print("Testing login functionality...")

# Create a request factory
factory = RequestFactory()

# Test with correct credentials
print("\n1. Testing with correct credentials...")
request = factory.post('/login/', {
    'email': 'test.auth@example.com',
    'password': 'testpassword123'
})

# Add session support
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore

middleware = SessionMiddleware(lambda req: None)
middleware.process_request(request)
request.session.save()

# Call the login view
response = login_page(request)

print(f"Response status code: {response.status_code}")
if response.status_code == 302:
    print("✓ Login successful - redirecting to donor dashboard")
    print(f"Session donor_id: {request.session.get('donor_id')}")
else:
    print("✗ Login failed")
    print(f"Response type: {type(response)}")

# Test with incorrect credentials
print("\n2. Testing with incorrect credentials...")
request = factory.post('/login/', {
    'email': 'test.auth@example.com',
    'password': 'wrongpassword'
})

# Add session support
middleware = SessionMiddleware(lambda req: None)
middleware.process_request(request)
request.session.save()

# Call the login view
response = login_page(request)

print(f"Response status code: {response.status_code}")
if response.status_code == 200:
    print("✓ Login correctly failed - showing login page with error")
    # Check if error message is in response content
    content = response.content.decode('utf-8')
    if 'Invalid email or password' in content:
        print("✓ Error message displayed correctly")
    else:
        print("✗ Error message not found in response")
else:
    print("✗ Unexpected response")