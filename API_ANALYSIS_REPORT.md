# FarmHub API Analysis Report

## Project Overview

FarmHub is a comprehensive farm management platform built with Django REST Framework (DRF) for the core service and FastAPI for the reporting service. The platform implements role-based access control with three main user roles: SuperAdmin, Agent, and Farmer.

## Architecture Analysis

### Core Service (Django REST Framework)
- **Port**: 8000
- **Database**: SQLite (development)
- **Authentication**: JWT tokens with SimpleJWT
- **Permissions**: Role-based access control

### Reporting Service (FastAPI)
- **Port**: 8001
- **Database**: Same SQLite database as core service
- **Purpose**: Read-only reporting and analytics
- **Authentication**: None (read-only service)

## User Roles and Permissions

### 1. SuperAdmin
- Full access to all endpoints
- Can create, read, update, delete all resources
- Can manage users, farms, cows, milk records, and activities

### 2. Agent
- Can manage farms assigned to them
- Can view farmers and cows under their farms
- Can view milk records and activities for their farms
- Cannot create/delete users (only SuperAdmin)

### 3. Farmer
- Can only manage their own cows
- Can record milk production for their cows
- Can log activities for their cows
- Cannot access other farmers' data

## API Endpoints Analysis

### Authentication Endpoints
1. **Custom Login** (`/api/users/login/`)
   - Returns user info + JWT tokens
   - Used for initial authentication

2. **JWT Token Login** (`/api/auth/token/`)
   - Standard JWT token endpoint
   - Returns access and refresh tokens

3. **Token Refresh** (`/api/auth/token/refresh/`)
   - Refresh expired access tokens

4. **Token Verify** (`/api/auth/token/verify/`)
   - Verify token validity

5. **Logout** (`/api/users/logout/`)
   - Blacklist refresh token

6. **Profile** (`/api/users/profile/`)
   - Get current user profile

7. **Change Password** (`/api/users/change_password/`)
   - Change user password

### User Management
- **CRUD Operations**: Full CRUD for users
- **Filtering**: By role, active status, staff status
- **Search**: By username, email, name, phone
- **Permissions**: SuperAdmin only for create/delete

### Farm Management
- **CRUD Operations**: Full CRUD for farms
- **Filtering**: By active status, agent role
- **Search**: By name, location, agent details
- **Permissions**: SuperAdmin and Agents

### Cow Management
- **CRUD Operations**: Full CRUD for cows
- **Filtering**: By breed, status, pregnancy, farmer, farm
- **Search**: By tag number, name, farmer details
- **Permissions**: Role-based access

### Milk Records
- **CRUD Operations**: Full CRUD for milk records
- **Special Endpoints**:
  - `record-daily/`: Record daily production for single cow
  - `bulk-record/`: Record production for multiple cows
  - `production-summary/`: Get production statistics
  - `cow-production/{tag}/`: Get cow-specific history
- **Filtering**: By date, quality, breed, farm
- **Permissions**: Role-based access

### Activities
- **CRUD Operations**: Full CRUD for activities
- **Special Endpoints**:
  - `log-activity/`: Log general activity
  - `log-vaccination/`: Log vaccination with details
  - `log-health-check/`: Log health check with status
  - `log-calving/`: Log calving with calf details
  - `activity-summary/`: Get activity statistics
  - `cow-activities/{tag}/`: Get cow-specific activities
  - `overdue-activities/`: Get overdue activities
  - `upcoming-activities/`: Get upcoming activities
- **Filtering**: By type, status, date, breed, farm
- **Permissions**: Role-based access

## FastAPI Reporting Service

### Data Access Endpoints
- **Users**: Get users with filtering by role
- **Farms**: Get farms with filtering by active status
- **Cows**: Get cows with filtering by breed, status, farm
- **Milk Records**: Get records with date range filtering
- **Activities**: Get activities with type and status filtering

### Reporting Endpoints
1. **Production Summary** (`/reports/production-summary`)
   - Total production statistics
   - Date range filtering
   - Farm-specific filtering

2. **Activity Summary** (`/reports/activity-summary`)
   - Activity statistics and costs
   - Type distribution
   - Date range filtering

3. **Farm Summary** (`/reports/farm-summary`)
   - Farm-specific statistics
   - Farmer and cow counts
   - Production totals

4. **Milk Production Filtered** (`/reports/milk-production`)
   - Detailed production data
   - Multiple filtering options
   - Related data included

5. **Recent Activities** (`/reports/recent-activities`)
   - Recent activity summaries
   - Daily breakdown
   - Completion statistics

## Updated Postman Collection Features

### 1. Enhanced Authentication
- **Variable-based credentials**: Uses collection variables for username/password
- **Automatic token management**: Test scripts automatically save tokens
- **Multiple auth methods**: Both custom login and JWT token endpoints

### 2. Comprehensive Coverage
- **All DRF endpoints**: Complete CRUD operations for all models
- **Special endpoints**: All custom actions and bulk operations
- **FastAPI endpoints**: All reporting service endpoints
- **Filtering examples**: Query parameter examples for all filterable endpoints

### 3. Additional Endpoints Section
- **Search examples**: User search, cow search by tag
- **Filtering examples**: Date ranges, activity types, farm filtering
- **Advanced queries**: Complex filtering combinations

### 4. Enhanced FastAPI Section
- **Individual resource endpoints**: Get by ID for all resources
- **Advanced filtering**: Multiple parameter combinations
- **Comprehensive reporting**: All report types with examples

### 5. Environment Variables
- **Base URLs**: Separate variables for DRF and FastAPI services
- **Token management**: Automatic token storage and retrieval
- **Credential management**: Centralized admin credentials

## Key Improvements Made

1. **Token Automation**: Added test scripts to automatically save tokens
2. **Variable Usage**: Replaced hardcoded values with collection variables
3. **Additional Endpoints**: Added missing endpoints found in code analysis
4. **Enhanced Documentation**: Updated descriptions and added context
5. **Filtering Examples**: Added comprehensive query parameter examples
6. **FastAPI Coverage**: Expanded FastAPI endpoint coverage
7. **Error Handling**: Added proper error response examples

## Usage Instructions

1. **Import Collection**: Import the updated JSON file into Postman
2. **Set Variables**: Update base URLs if needed (defaults to localhost)
3. **Authenticate**: Use the Login endpoints to get tokens
4. **Test Endpoints**: Tokens will be automatically used for authenticated requests
5. **Explore Features**: Use the various filtering and search capabilities

## Security Considerations

- **Role-based Access**: All endpoints implement proper role-based permissions
- **Token Management**: JWT tokens with proper refresh mechanisms
- **Input Validation**: All endpoints include proper validation
- **Data Isolation**: Users can only access their authorized data

## Performance Features

- **Filtering**: Efficient database filtering on all endpoints
- **Pagination**: Built-in pagination support
- **Search**: Full-text search capabilities
- **Caching**: FastAPI service optimized for read operations

This updated collection provides comprehensive coverage of the FarmHub API ecosystem, making it easy to test and explore all available functionality.
