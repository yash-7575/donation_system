#!/usr/bin/env python
import requests
import json

# Test the JOIN operations endpoints
base_url = "http://127.0.0.1:8000/api"

join_types = ['equijoin', 'non-equijoin', 'self-join', 'natural-join', 'left-join', 'right-join', 'full-join']

print("Testing JOIN Operations API:")
print("="*50)

for join_type in join_types:
    print(f"\nTesting {join_type}:")
    try:
        response = requests.get(f"{base_url}/joins/{join_type}/")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                results = data['results']
                print(f"  ✓ Success: {len(results)} rows returned")
                if results:
                    # Show first result as sample
                    sample = results[0]
                    print(f"  Sample result: {sample}")
                else:
                    print("  No data returned")
            else:
                print(f"  ✗ API Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"  ✗ HTTP Error: {response.status_code}")
            print(f"    Response: {response.text[:200]}")
    except Exception as e:
        print(f"  ✗ Exception: {str(e)}")

print("\n" + "="*50)
print("JOIN Operations API testing completed!")