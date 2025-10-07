#!/usr/bin/env python
import requests
import json

# Check which donors have donations
base_url = "http://127.0.0.1:8000/api"

print("Testing donations for all donors:")
response = requests.get(f"{base_url}/donors/")
if response.status_code == 200:
    donors = response.json()
    for donor in donors:
        donor_id = donor['donor_id']
        donations_response = requests.get(f"{base_url}/donors/{donor_id}/donations/")
        if donations_response.status_code == 200:
            donations = donations_response.json()
            print(f"Donor {donor_id} ({donor['name']}): {len(donations)} donations")
            if donations:
                for donation in donations[:2]:  # Show first 2
                    print(f"  - {donation['title']} ({donation['status']}) - {donation['category']}")
        else:
            print(f"Error for donor {donor_id}: {donations_response.status_code}")

# Also check all donations to see donor IDs
print("\nAll donations with donor IDs:")
all_donations_response = requests.get(f"{base_url}/donations/")
if all_donations_response.status_code == 200:
    all_donations = all_donations_response.json()
    donor_counts = {}
    for donation in all_donations:
        donor_id = donation['donor']
        donor_counts[donor_id] = donor_counts.get(donor_id, 0) + 1
    
    print("Donations by donor ID:")
    for donor_id, count in donor_counts.items():
        print(f"  Donor {donor_id}: {count} donations")