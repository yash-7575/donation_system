#!/usr/bin/env python
import requests
import json

def test_complete_donation_chain():
    """Test the complete donation chain from login to display"""
    base_url = "http://127.0.0.1:8000"
    
    print("🔗 TESTING COMPLETE DONATION CHAIN")
    print("=" * 60)
    
    # Test 1: Check if we can access the donor dashboard directly
    print("\n1. Testing donor dashboard access...")
    try:
        # We'll test with a session by trying to login first
        session = requests.Session()
        
        # Try to get the login page first
        login_response = session.get(f"{base_url}/login/")
        print(f"   Login page status: {login_response.status_code}")
        
        # Let's try to simulate what happens when accessing dashboard directly
        dashboard_response = session.get(f"{base_url}/donor/")
        print(f"   Dashboard access status: {dashboard_response.status_code}")
        print(f"   Dashboard redirects to: {dashboard_response.url}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Check API endpoints individually
    print("\n2. Testing API endpoints...")
    
    # Test donor with donations (donor 3)
    test_donor_id = 3
    print(f"   Testing donor {test_donor_id}:")
    
    try:
        # Test donor detail
        donor_response = requests.get(f"{base_url}/api/donors/{test_donor_id}/")
        print(f"     Donor detail: {donor_response.status_code}")
        if donor_response.status_code == 200:
            donor_data = donor_response.json()
            print(f"     Donor name: {donor_data.get('name', 'Unknown')}")
        
        # Test donor donations
        donations_response = requests.get(f"{base_url}/api/donors/{test_donor_id}/donations/")
        print(f"     Donor donations: {donations_response.status_code}")
        if donations_response.status_code == 200:
            donations = donations_response.json()
            print(f"     Number of donations: {len(donations)}")
            if donations:
                print(f"     Sample donation: {donations[0]['title']}")
        else:
            print(f"     Error response: {donations_response.text}")
            
    except Exception as e:
        print(f"     ❌ API Error: {e}")
    
    # Test 3: Check if the issue is in template context
    print("\n3. Analyzing potential issues...")
    print("   Possible issues:")
    print("   - User not logged in (session not set)")
    print("   - JavaScript getCurrentUserId() function not finding ID")
    print("   - Template context not passing donor.donor_id correctly")
    print("   - API call failing due to CORS or authentication")
    
    # Test 4: Check CSRF and other headers
    print("\n4. Testing request headers...")
    try:
        response = requests.get(f"{base_url}/api/donors/3/donations/", headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        print(f"   With proper headers: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Headers test error: {e}")
    
    print("\n" + "=" * 60)
    print("📋 RECOMMENDATIONS:")
    print("1. Ensure user is properly logged in")
    print("2. Check browser console for JavaScript errors")
    print("3. Verify window.CURRENT_USER_ID is set in browser")
    print("4. Check if loadDonations() is being called")
    print("5. Verify API endpoint is reachable")

if __name__ == "__main__":
    test_complete_donation_chain()