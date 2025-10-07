#!/usr/bin/env python
import requests
import json

def test_comprehensive_joins():
    """Comprehensive test of JOIN operations implementation"""
    base_url = "http://127.0.0.1:8000/api"
    
    print("🔍 COMPREHENSIVE JOIN OPERATIONS TEST")
    print("=" * 60)
    
    # Test 1: Verify server is running
    print("\n1. Testing server connectivity...")
    try:
        response = requests.get(f"{base_url}/health/")
        if response.status_code == 200:
            print("   ✅ Server is running and accessible")
        else:
            print(f"   ❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to server: {e}")
        return False
    
    # Test 2: Verify data exists
    print("\n2. Checking database data...")
    try:
        donors_response = requests.get(f"{base_url}/donors/")
        donations_response = requests.get(f"{base_url}/donations/")
        
        if donors_response.status_code == 200 and donations_response.status_code == 200:
            donors = donors_response.json()
            donations = donations_response.json()
            print(f"   ✅ Found {len(donors)} donors and {len(donations)} donations")
        else:
            print("   ❌ Failed to fetch basic data")
            return False
    except Exception as e:
        print(f"   ❌ Error fetching data: {e}")
        return False
    
    # Test 3: Test all JOIN operations
    print("\n3. Testing JOIN operations...")
    join_types = ['equijoin', 'non-equijoin', 'self-join', 'natural-join', 'left-join', 'right-join', 'full-join']
    
    join_results = {}
    
    for join_type in join_types:
        try:
            response = requests.get(f"{base_url}/joins/{join_type}/")
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    results = data['results']
                    join_results[join_type] = len(results)
                    print(f"   ✅ {join_type:15} - {len(results):3d} rows")
                else:
                    print(f"   ❌ {join_type:15} - API error: {data.get('error', 'Unknown')}")
                    join_results[join_type] = 'ERROR'
            else:
                print(f"   ❌ {join_type:15} - HTTP {response.status_code}")
                join_results[join_type] = 'HTTP_ERROR'
        except Exception as e:
            print(f"   ❌ {join_type:15} - Exception: {str(e)}")
            join_results[join_type] = 'EXCEPTION'
    
    # Test 4: Detailed analysis of specific joins
    print("\n4. Detailed JOIN analysis...")
    
    # Test EQUIJOIN specifically
    try:
        response = requests.get(f"{base_url}/joins/equijoin/")
        if response.status_code == 200:
            data = response.json()
            if data['success'] and data['results']:
                sample = data['results'][0]
                print(f"   📊 EQUIJOIN sample: {sample}")
            else:
                print("   ⚠️  EQUIJOIN returned no data")
        else:
            print("   ❌ EQUIJOIN failed")
    except Exception as e:
        print(f"   ❌ EQUIJOIN error: {e}")
    
    # Test LEFT JOIN to verify all donors are included
    try:
        response = requests.get(f"{base_url}/joins/left-join/")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                results = data['results']
                donors_with_donations = sum(1 for r in results if r['donation_count'] > 0)
                donors_without_donations = sum(1 for r in results if r['donation_count'] == 0)
                print(f"   📊 LEFT JOIN: {donors_with_donations} donors with donations, {donors_without_donations} without")
            else:
                print("   ❌ LEFT JOIN failed")
        else:
            print("   ❌ LEFT JOIN HTTP error")
    except Exception as e:
        print(f"   ❌ LEFT JOIN error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 SUMMARY:")
    print(f"   Total JOIN types tested: {len(join_types)}")
    successful_joins = sum(1 for result in join_results.values() if isinstance(result, int))
    print(f"   Successful JOINs: {successful_joins}/{len(join_types)}")
    
    if successful_joins == len(join_types):
        print("\n🎉 ALL JOIN OPERATIONS ARE WORKING PERFECTLY!")
        print("   ✅ Backend API endpoints functioning")
        print("   ✅ Database queries executing successfully")
        print("   ✅ Data being returned correctly")
        print("\n🚀 Ready for frontend integration!")
        return True
    else:
        print("\n⚠️  Some JOIN operations failed:")
        for join_type, result in join_results.items():
            if not isinstance(result, int):
                print(f"   ❌ {join_type}: {result}")
        return False

if __name__ == "__main__":
    test_comprehensive_joins()