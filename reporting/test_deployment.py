#!/usr/bin/env python
"""
Test script to verify deployment configuration
"""

import sys
import os

def test_main_import():
    """Test if main.py can be imported successfully"""
    try:
        from main import app
        print("✅ Successfully imported main:app")
        
        # Count the number of routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        print(f"✅ Found {len(routes)} routes in the application")
        print("Routes found:")
        for route in routes:
            print(f"  - {route}")
            
        return True
    except Exception as e:
        print(f"❌ Failed to import main:app: {e}")
        return False

def test_minimal_import():
    """Test if main_minimal.py can be imported"""
    try:
        from main_minimal import app
        print("✅ Successfully imported main_minimal:app")
        
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        print(f"⚠️  Found {len(routes)} routes in minimal app (should be 3)")
        return True
    except Exception as e:
        print(f"❌ Failed to import main_minimal:app: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        from database import test_connection
        if test_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

if __name__ == "__main__":
    print("Testing FarmHub Reporting Service deployment configuration...")
    print("=" * 60)
    
    # Test main app import
    main_ok = test_main_import()
    print()
    
    # Test minimal app import
    minimal_ok = test_minimal_import()
    print()
    
    # Test database connection
    db_ok = test_database_connection()
    print()
    
    print("=" * 60)
    if main_ok and db_ok:
        print("✅ All tests passed! Deployment should work correctly.")
        print("💡 Use 'python start_production.py' for deployment")
    else:
        print("❌ Some tests failed. Please check the configuration.")
        sys.exit(1)
