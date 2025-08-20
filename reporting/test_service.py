#!/usr/bin/env python
"""
Test script for the FastAPI reporting service
"""

import requests
import json
import sys

def test_reporting_service():
    """Test the FastAPI reporting service endpoints"""
    base_url = "http://localhost:8001"
    
    print("Testing FarmHub Reporting Service...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Health Check: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"  Status: {health_data.get('status')}")
            print(f"  Database: {health_data.get('database')}")
        print()
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        print("Make sure the service is running on port 8001")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"Root Endpoint: {response.status_code}")
        if response.status_code == 200:
            root_data = response.json()
            print(f"  Service: {root_data.get('service')}")
            print(f"  Version: {root_data.get('version')}")
        print()
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint failed: {e}")
        return False
    
    # Test data endpoints
    endpoints = [
        '/users',
        '/farms', 
        '/cows',
        '/milk-records',
        '/activities'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}?limit=5", timeout=5)
            print(f"{endpoint}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Records found: {len(data)}")
            elif response.status_code == 404:
                print("  No records found (expected for empty database)")
            else:
                print(f"  Unexpected status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Error: {e}")
        print()
    
    # Test reporting endpoints
    report_endpoints = [
        '/reports/production-summary',
        '/reports/activity-summary'
    ]
    
    for endpoint in report_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"{endpoint}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Report generated successfully")
                if 'total_records' in data:
                    print(f"  Total records: {data['total_records']}")
                if 'total_activities' in data:
                    print(f"  Total activities: {data['total_activities']}")
            else:
                print(f"  Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Error: {e}")
        print()
    
    print("✅ FastAPI service testing completed!")
    return True

if __name__ == "__main__":
    success = test_reporting_service()
    if not success:
        sys.exit(1)
