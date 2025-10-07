#!/usr/bin/env python
import requests
import json

def test_donor_donations_endpoint():
    """Test the donor_donations endpoint and identify issues"""
    base_url = "http://127.0.0.1:8000/api"
    
    print("🔍 TESTING DONOR DONATIONS ENDPOINT")
    print("=" * 50)
    
    # Test 1: Get all donors first
    print("\n1. Getting all donors...")
    try:
        response = requests.get(f"{base_url}/donors/")
        if response.status_code == 200:
            donors = response.json()
            print(f"   ✅ Found {len(donors)} donors")
            for donor in donors:
                print(f"      - Donor {donor['donor_id']}: {donor['name']} ({donor['email']})")
        else:
            print(f"   ❌ Failed to get donors: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error getting donors: {e}")
        return False
    
    # Test 2: Test donor_donations for each donor
    print("\n2. Testing donor_donations endpoint for each donor...")
    for donor in donors:
        donor_id = donor['donor_id']
        print(f"\n   Testing donor {donor_id} ({donor['name']}):")
        
        try:
            response = requests.get(f"{base_url}/donors/{donor_id}/donations/")
            print(f"     Status Code: {response.status_code}")
            
            if response.status_code == 200:
                donations = response.json()
                print(f"     ✅ Success: {len(donations)} donations found")
                
                if donations:
                    print("     Sample donation:")
                    sample = donations[0]
                    for key, value in sample.items():
                        print(f"       {key}: {value}")
                else:
                    print("     📝 No donations for this donor")
            else:
                print(f"     ❌ HTTP Error: {response.status_code}")
                print(f"     Response: {response.text}")
                
        except Exception as e:
            print(f"     ❌ Exception: {str(e)}")
    
    # Test 3: Test the frontend JavaScript getCurrentUserId function
    print("\n3. Testing user ID detection...")
    print("   The issue might be in the getCurrentUserId() function")
    print("   Let's check if window.CURRENT_USER_ID is properly set")
    
    return True

if __name__ == "__main__":
    test_donor_donations_endpoint()