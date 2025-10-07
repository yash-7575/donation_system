#!/usr/bin/env python
import requests
import json

# Test the new donations endpoint
base_url = "http://127.0.0.1:8000/api"

# First, get all donors to see which ones exist
print("Testing Donors API:")
response = requests.get(f"{base_url}/donors/")
if response.status_code == 200:
    donors = response.json()
    print(f"Found {len(donors)} donors:")
    for donor in donors[:3]:  # Show first 3
        print(f"  - Donor {donor['donor_id']}: {donor['name']} ({donor['email']})")
    
    # Test donations for first donor
    if donors:
        first_donor_id = donors[0]['donor_id']
        print(f"\nTesting donations for donor {first_donor_id}:")
        
        donations_response = requests.get(f"{base_url}/donors/{first_donor_id}/donations/")
        if donations_response.status_code == 200:
            donations = donations_response.json()
            print(f"Found {len(donations)} donations:")
            for donation in donations:
                print(f"  - Donation {donation['donation_id']}: {donation['title']} ({donation['status']})")
        else:
            print(f"Error getting donations: {donations_response.status_code}")
            print(donations_response.text)
else:
    print(f"Error getting donors: {response.status_code}")
    print(response.text)

# Test all donations endpoint
print(f"\nTesting all donations:")
all_donations_response = requests.get(f"{base_url}/donations/")
if all_donations_response.status_code == 200:
    all_donations = all_donations_response.json()
    print(f"Found {len(all_donations)} total donations")
else:
    print(f"Error getting all donations: {all_donations_response.status_code}")