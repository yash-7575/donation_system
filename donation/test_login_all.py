import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.test import RequestFactory
from frontend.views import login_page

# Test login functionality for all user types
print("Testing login functionality for all user types...")

# Create a request factory
factory = RequestFactory()

# Test donor login
print("\n1. Testing donor login with correct credentials...")
request = factory.post('/login/', {
    'email': 'test.donor@example.com',
    'password': 'donorpass123',
    'role': 'donor'
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
    print("✓ Donor login successful - redirecting to donor dashboard")
    print(f"Session user_id: {request.session.get('user_id')}")
    print(f"Session user_type: {request.session.get('user_type')}")
else:
    print("✗ Donor login failed")
    print(f"Response type: {type(response)}")

# Test recipient login
print("\n2. Testing recipient login with correct credentials...")
request = factory.post('/login/', {
    'email': 'test.recipient@example.com',
    'password': 'recipientpass123',
    'role': 'recipient'
})

# Add session support
middleware = SessionMiddleware(lambda req: None)
middleware.process_request(request)
request.session.save()

# Call the login view
response = login_page(request)

print(f"Response status code: {response.status_code}")
if response.status_code == 302:
    print("✓ Recipient login successful - redirecting to recipient dashboard")
    print(f"Session user_id: {request.session.get('user_id')}")
    print(f"Session user_type: {request.session.get('user_type')}")
else:
    print("✗ Recipient login failed")
    print(f"Response type: {type(response)}")

# Test NGO login
print("\n3. Testing NGO login with correct credentials...")
request = factory.post('/login/', {
    'email': 'test.ngo@example.com',
    'password': 'ngopass123',
    'role': 'ngo_admin'
})

# Add session support
middleware = SessionMiddleware(lambda req: None)
middleware.process_request(request)
request.session.save()

# Call the login view
response = login_page(request)

print(f"Response status code: {response.status_code}")
if response.status_code == 302:
    print("✓ NGO login successful - redirecting to NGO dashboard")
    print(f"Session user_id: {request.session.get('user_id')}")
    print(f"Session user_type: {request.session.get('user_type')}")
else:
    print("✗ NGO login failed")
    print(f"Response type: {type(response)}")

# Test failed login
print("\n4. Testing failed login with incorrect credentials...")
request = factory.post('/login/', {
    'email': 'test.donor@example.com',
    'password': 'wrongpassword',
    'role': 'donor'
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

print("\n✓ All login tests completed!")