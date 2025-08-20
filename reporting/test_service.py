#!/usr/bin/env python
"""
Test script for the FastAPI reporting service
"""

import requests
import json
import sys
from datetime import date, timedelta

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
            print(f"  New endpoints available: {len([k for k in root_data.get('endpoints', {}).keys() if k in ['farm_summary', 'milk_production', 'recent_activities']])}")
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
    
    # Test basic reporting endpoints
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
    
    # Test NEW reporting endpoints
    print("Testing NEW Reporting Endpoints...")
    print("-" * 30)
    
    # Test farm summary endpoint
    try:
        response = requests.get(f"{base_url}/reports/farm-summary", timeout=5)
        print(f"Farm Summary: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'overall_summary' in data:
                print(f"  Overall farms: {data['overall_summary'].get('total_farms', 0)}")
                print(f"  Total farmers: {data['overall_summary'].get('total_farmers', 0)}")
                print(f"  Total cows: {data['overall_summary'].get('total_cows', 0)}")
                print(f"  Total milk: {data['overall_summary'].get('total_milk_production_liters', 0):.2f}L")
            else:
                print(f"  Single farm data retrieved")
        else:
            print(f"  Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error: {e}")
    print()
    
    # Test milk production filtering endpoint
    try:
        # Test with date range
        from_date = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
        to_date = date.today().strftime('%Y-%m-%d')
        
        response = requests.get(
            f"{base_url}/reports/milk-production",
            params={
                'from_date': from_date,
                'to_date': to_date,
                'limit': 10
            },
            timeout=5
        )
        print(f"Milk Production Filtered: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Records found: {data['summary'].get('total_records', 0)}")
            print(f"  Total quantity: {data['summary'].get('total_quantity_liters', 0):.2f}L")
            print(f"  Average quantity: {data['summary'].get('average_quantity_liters', 0):.2f}L")
            print(f"  Filters applied: {data['filters_applied']}")
        else:
            print(f"  Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error: {e}")
    print()
    
    # Test recent activities endpoint
    try:
        response = requests.get(
            f"{base_url}/reports/recent-activities",
            params={
                'days': 7,
                'limit': 10
            },
            timeout=5
        )
        print(f"Recent Activities: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Activities found: {data['summary'].get('total_activities', 0)}")
            print(f"  Completed: {data['summary'].get('completed_activities', 0)}")
            print(f"  Planned: {data['summary'].get('planned_activities', 0)}")
            print(f"  Completion rate: {data['summary'].get('completion_rate', 0):.1f}%")
            print(f"  Total cost: ${data['summary'].get('total_cost', 0):.2f}")
            print(f"  Date range: {data['date_range']['start_date']} to {data['date_range']['end_date']}")
        else:
            print(f"  Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error: {e}")
    print()
    
    # Test specific farm summary
    try:
        response = requests.get(f"{base_url}/reports/farm-summary?farm_id=1", timeout=5)
        print(f"Specific Farm Summary (ID=1): {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Farm: {data.get('farm_name', 'Unknown')}")
            print(f"  Farmers: {data.get('farmer_count', 0)}")
            print(f"  Cows: {data.get('cow_count', 0)}")
            print(f"  Total milk: {data.get('total_milk_production_liters', 0):.2f}L")
        elif response.status_code == 404:
            print("  Farm not found (expected if no data)")
        else:
            print(f"  Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error: {e}")
    print()
    
    print("✅ FastAPI service testing completed!")
    print("=" * 50)
    print("📊 New endpoints tested:")
    print("  • /reports/farm-summary - Farm summaries with farmer/cow counts")
    print("  • /reports/milk-production - Filtered milk production data")
    print("  • /reports/recent-activities - Recent activity summaries")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = test_reporting_service()
    if not success:
        sys.exit(1)
