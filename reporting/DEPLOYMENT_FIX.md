# FarmHub Reporting Service - Deployment Fix

## Issue Description
The FastAPI reporting service was only showing 3 basic endpoints (`/`, `/health`, `/test`) on Render deployment instead of the full set of 25+ endpoints available locally.

## Root Cause
Multiple start scripts were using `main_minimal:app` instead of `main:app`:
- `start_render.py` was using `main_minimal:app`
- `start_simple_render.py` was using `main_minimal:app`
- `main_minimal.py` only contains 3 basic endpoints

## Solution Applied

### 1. Fixed Start Scripts
- Updated `start_render.py` to use `main:app` instead of `main_minimal:app`
- Updated `start_simple_render.py` to use `main:app` instead of `main_minimal:app`

### 2. Updated Render Configuration
- Changed `render.yaml` to use `start_production.py` which correctly imports from `main:app`
- This ensures the full FastAPI application with all endpoints is deployed

### 3. Added Warnings
- Added warning comment to `main_minimal.py` to prevent future misuse
- Updated documentation in start scripts

## Files Modified
1. `reporting/start_render.py` - Fixed to use main:app
2. `reporting/start_simple_render.py` - Fixed to use main:app  
3. `render.yaml` - Updated to use start_production.py
4. `reporting/main_minimal.py` - Added warning comment

## Verification
After deployment, the service should show all endpoints:
- User endpoints: `/users`, `/users/{user_id}`
- Farm endpoints: `/farms`, `/farms/{farm_id}`
- Cow endpoints: `/cows`, `/cows/{cow_id}`
- Milk record endpoints: `/milk-records`
- Activity endpoints: `/activities`
- Reporting endpoints: `/reports/production-summary`, `/reports/activity-summary`, etc.

## Recommended Deployment Command
Use `start_production.py` for production deployments as it:
- Imports the full app from `main.py`
- Provides proper logging
- Handles environment variables correctly
- Shows database connection status
