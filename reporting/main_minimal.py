"""
Minimal FastAPI app for Render deployment
WARNING: This is a minimal version with only basic endpoints.
For production deployment, use main.py instead.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Initialize FastAPI app
app = FastAPI(
    title="FarmHub Reporting Service",
    description="Read-only reporting service for FarmHub farm management platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Service information"""
    return {
        "service": "FarmHub Reporting Service",
        "version": "1.0.0",
        "description": "Read-only reporting service for farm management analytics",
        "docs": "/docs",
        "status": "deployed"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Service is running",
        "port": os.environ.get("PORT", "unknown")
    }

@app.get("/test")
async def test():
    """Test endpoint"""
    return {"message": "API is working!"}
