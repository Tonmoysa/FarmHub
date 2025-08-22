#!/usr/bin/env python
"""
Test database configuration
"""

import os
import sys

def test_database_import():
    """Test if database module can be imported"""
    try:
        from database import get_db, SessionLocal, test_connection
        print("✅ Successfully imported database module")
        return True
    except Exception as e:
        print(f"❌ Failed to import database module: {e}")
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

def test_main_import():
    """Test if main.py can be imported with database dependencies"""
    try:
        from main import app
        print("✅ Successfully imported main:app with database dependencies")
        return True
    except Exception as e:
        print(f"❌ Failed to import main:app: {e}")
        return False

if __name__ == "__main__":
    print("Testing database configuration...")
    print("=" * 50)
    
    # Test database import
    db_import_ok = test_database_import()
    print()
    
    # Test database connection
    db_conn_ok = test_database_connection()
    print()
    
    # Test main import
    main_ok = test_main_import()
    print()
    
    print("=" * 50)
    if db_import_ok and db_conn_ok and main_ok:
        print("✅ All database tests passed!")
    else:
        print("❌ Some database tests failed.")
        sys.exit(1)
