#!/usr/bin/env python
import requests
import json

def test_api_endpoints():
    """Test the API endpoints"""
    base_url = "http://localhost:8000/api/"
    
    # Test API root
    try:
        response = requests.get(base_url)
        print(f"API Root Status: {response.status_code}")
        if response.status_code == 200:
            print("API Root Response:", response.json())
        print()
    except Exception as e:
        print(f"Error accessing API root: {e}")
        return
    
    # Test endpoints that should be accessible
    endpoints = [
        'users/',
        'farms/',
        'cows/',
        'milk-records/',
        'activities/'
    ]
    
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            response = requests.get(url)
            print(f"{endpoint} Status: {response.status_code}")
            if response.status_code == 401:
                print("  ✓ Authentication required (expected)")
            elif response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                print(f"  ✓ Found {count} records")
            else:
                print(f"  ✗ Unexpected status: {response.status_code}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        print()

if __name__ == "__main__":
    print("Testing FarmHub API Endpoints...")
    print("=" * 40)
    test_api_endpoints()
    print("API testing completed!")
