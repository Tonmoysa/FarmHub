#!/usr/bin/env python
"""
Production startup script for the FastAPI reporting service on Render
"""

import uvicorn
import os

def start_production_service():
    """Start the FastAPI reporting service in production mode"""
    print("Starting FarmHub Reporting Service in production mode...")
    
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Use 0.0.0.0 to bind to all available network interfaces
    host = "0.0.0.0"
    
    print(f"Service will be available at: http://0.0.0.0:{port}")
    print(f"API Documentation: http://0.0.0.0:{port}/docs")
    print(f"Health Check: http://0.0.0.0:{port}/health")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=False,  # Disable reload in production
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"Error starting service: {e}")
        raise

if __name__ == "__main__":
    start_production_service()
