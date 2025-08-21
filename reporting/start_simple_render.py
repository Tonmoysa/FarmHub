#!/usr/bin/env python
"""
Ultra-simple startup script for Render deployment
"""

import os
import subprocess
import sys

if __name__ == "__main__":
    port = os.environ.get("PORT", "8000")
    print(f"Starting server on port {port}")
    
    try:
        # Use subprocess to run uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn",
            "main_minimal:app",
            "--host", "0.0.0.0",
            "--port", port
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
