#!/usr/bin/env python
"""
Startup script for the FastAPI reporting service
"""

import uvicorn
import sys
import os

def start_service():
    """Start the FastAPI reporting service"""
    print("Starting FarmHub Reporting Service...")
    print("Service will be available at: http://localhost:8001")
    print("API Documentation: http://localhost:8001/docs")
    print("Health Check: http://localhost:8001/health")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8001,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\nService stopped by user")
    except Exception as e:
        print(f"Error starting service: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_service()
