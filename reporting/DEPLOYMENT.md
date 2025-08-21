# FarmHub Reporting API - Render Deployment Guide

## Overview
This FastAPI service provides read-only reporting endpoints for the FarmHub farm management platform.

## Deployment on Render

### Option 1: Using render.yaml (Recommended)
1. Push your code to a Git repository (GitHub, GitLab, etc.)
2. Connect your repository to Render
3. Render will automatically detect the `render.yaml` file and deploy your service

### Option 2: Manual Deployment
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" and select "Web Service"
3. Connect your Git repository
4. Configure the service:
   - **Name**: `farmhub-reporting-api`
   - **Environment**: `Python`
   - **Build Command**: `cd reporting && pip install -r requirements-render.txt`
   - **Start Command**: `cd reporting && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`

### Environment Variables
Set these in your Render service settings:

- `DATABASE_URL`: Your PostgreSQL database connection string
  - Format: `postgresql://username:password@host:port/database`
  - You can use Render's PostgreSQL service or external database

### Build and Start Commands

**Build Command:**
```bash
cd reporting && pip install -r requirements-render.txt
```

**Start Command:**
```bash
cd reporting && python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Alternative Start Commands
You can also use the production script:
```bash
cd reporting && python start_production.py
```

Or directly with uvicorn:
```bash
cd reporting && python -m uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
```

## Service Endpoints
- **Root**: `/` - Service information
- **Health Check**: `/health` - Database connection status
- **API Docs**: `/docs` - Interactive API documentation
- **Users**: `/users` - Get all users
- **Farms**: `/farms` - Get all farms
- **Cows**: `/cows` - Get all cows
- **Milk Records**: `/milk-records` - Get milk production records
- **Activities**: `/activities` - Get farm activities

## Database Requirements
- PostgreSQL database (recommended for production)
- The service connects to your Django database in read-only mode
- Ensure your database is accessible from Render's servers

## Troubleshooting
1. **Build fails**: 
   - Use `requirements-render.txt` for Render deployment (avoids Rust compilation issues)
   - Check that all dependencies are in the requirements file
2. **Start fails**: Verify the `DATABASE_URL` environment variable is set correctly
3. **Database connection fails**: Ensure your database allows connections from Render's IP ranges
4. **Port issues**: Render automatically sets the `PORT` environment variable

## Local Development
To run locally:
```bash
cd reporting
pip install -r requirements.txt  # Use original requirements for local development
python start_service.py
```

The service will be available at `http://localhost:8001`
