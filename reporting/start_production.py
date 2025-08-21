#!/usr/bin/env python
"""
Production startup script for Render deployment
Loads the full FastAPI app with all endpoints
"""

import os
import uvicorn
from main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting FarmHub Reporting Service on {host}:{port}")
    print(f"Database URL: {os.environ.get('DATABASE_URL', 'Not set')}")
    
    # Start the server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
