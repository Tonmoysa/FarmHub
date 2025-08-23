# FarmHub

A comprehensive farm management platform designed for agritech companies. FarmHub enables farm registration, farmer onboarding, cow enrollment, and daily operations tracking including milk production and health-related activities.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Directory Layout](#directory-layout)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Local Setup](#local-setup)
- [Database & Seed Data](#database--seed-data)
- [Role-Based Access](#role-based-access)
- [Django Admin](#django-admin)
- [API Reference - Core (DRF)](#api-reference---core-drf)
- [API Reference - Reporting (FastAPI)](#api-reference---reporting-fastapi)
- [Postman Collection](#postman-collection)
- [Docker/Compose](#dockercompose)
- [Deployment Notes](#deployment-notes)
- [Troubleshooting](#troubleshooting)

## Overview

FarmHub is a farm management platform built with Django backend and FastAPI reporting microservice. The platform demonstrates robust data model design, role-based access control, REST APIs using Django REST Framework (DRF), Django Admin configuration for non-technical users, and a read-only reporting service using FastAPI.

### Key Features
- Multi-role user management (SuperAdmin, Agent, Farmer)
- Farm registration and management
- Farmer onboarding and assignment
- Cow enrollment and tracking
- Daily milk production recording
- Health-related activities tracking
- Real-time reporting and analytics
- RESTful API architecture

## Architecture

FarmHub consists of two main services:

### Core Service (Django + DRF)
- **Location**: `/core/`
- **Purpose**: Main application logic, data management, and CRUD operations
- **Technology**: Django 5.2.5 + Django REST Framework + JWT Authentication
- **Database**: PostgreSQL (production) / SQLite (development)
- **Port**: 8000 (default)

### Reporting Service (FastAPI)
- **Location**: `/reporting/`
- **Purpose**: Read-only reporting and analytics
- **Technology**: FastAPI + SQLAlchemy + Pydantic
- **Database**: Shares the same database as Django core
- **Port**: 8001 (default)

## Directory Layout

```
FarmHub/
├── core/                    # Django core service
│   ├── users/              # User management
│   ├── farms/              # Farm management
│   ├── cows/               # Livestock management
│   ├── milk/               # Milk production
│   ├── activities/         # Activity tracking
│   ├── fixtures/           # Seed data
│   ├── core_service/       # Django settings
│   ├── requirements.txt    # Python dependencies
│   ├── runtime.txt         # Python version
│   └── manage.py           # Django management
├── reporting/              # FastAPI reporting service
│   ├── main.py            # FastAPI application
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── database.py        # Database connection
│   ├── requirements.txt   # Python dependencies
│   └── start_simple_render.py # Production startup
├── render.yaml            # Render deployment config
├── env.example            # Environment variables template
├── runtime.txt            # Root Python version
└── README.md              # This file
```

## Prerequisites

- **Python**: 3.11.18 (as specified in runtime.txt)
- **pip**: Latest version
- **virtualenv**: For environment isolation
- **uvicorn**: For FastAPI service (included in requirements)
- **PostgreSQL**: For production deployment
- **SQLite**: For local development (included with Python)

## Environment Variables

Create a `.env` file in the root directory based on `env.example`:

```bash
# Django Core Service Environment Variables
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com

# Production PostgreSQL Database URL for Render
DATABASE_URL=postgresql://farmhub_3l2z_user:QCTGvShsswsHjotWftVYt6RktgLGPRht@dpg-d2jidgn5r7bs73eu3k80-a.frankfurt-postgres.render.com:5432/farmhub_3l2z

# Superuser Configuration (for automatic deployment setup)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@farmhub.com
DJANGO_SUPERUSER_PASSWORD=admin123

# FastAPI Reporting Service Environment Variables
# Uses the same DATABASE_URL as Django for production
# For local development, FastAPI will use: sqlite:///../core/db.sqlite3
```

## Local Setup

### 1. Clone and Setup
```bash
git clone <repository-url>
cd FarmHub
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Core Django service
cd core
pip install -r requirements.txt

# Reporting service
cd ../reporting
pip install -r requirements.txt
cd ..
```

### 4. Database Setup
```bash
cd core
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
```

### 5. Run Services

#### Django Core Service (Port 8000)
```bash
cd core
python manage.py runserver
```

#### FastAPI Reporting Service (Port 8001)
```bash
cd reporting
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

## Database & Seed Data

The system comes pre-loaded with sample data via `core/fixtures/initial_data.json`:

### Users
- **SuperAdmin**: `admin` / `admin123`
- **Agent**: `agent1` / `agent123`
- **Farmer**: `farmer1` / `farmer123`

### Sample Data
- **1 Farm**: Green Valley Farm (150 acres)
- **2 Cows**: 
  - COW001 (Bessie) - Holstein breed
  - COW002 (Daisy) - Jersey breed (pregnant)
- **3 Milk Records**: Production data with quality metrics
- **3 Activities**: Vaccination, health check, maintenance

### Loading Seed Data
```bash
cd core
python manage.py loaddata fixtures/initial_data.json
```

## Role-Based Access

The platform implements three primary roles with role-based access control:

### 1. SuperAdmin
- **Permissions**: Full system access
- **Can CRUD**: All users, farms, cows, milk records, activities
- **Responsibilities**: System-wide oversight and user management

### 2. Agent
- **Permissions**: Manage assigned farms only
- **Can CRUD**: Farmers assigned to their farms, farm data, view assigned farms' cows and records
- **Responsibilities**: Farm oversight, farmer coordination, regional management

### 3. Farmer
- **Permissions**: Manage own cows and records
- **Can CRUD**: Own cows, own milk records, own activities
- **Responsibilities**: Daily operations, milk recording, livestock care

## Django Admin

The Django Admin interface is configured for non-technical users with:

- **User-friendly interface** for all models (Users, Farms, Cows, Milk Records, Activities)
- **Search functionality** across all fields
- **Filtering options** by status, date, role, etc.
- **Inline editing** for related models
- **Role-based access** - different views for different user types
- **Bulk operations** for efficient data management

### Access Django Admin:
- **URL**: `http://localhost:8000/admin/`
- **SuperAdmin Login**: `admin` / `admin123`
- **Features**: Complete CRUD operations with intuitive interface

## API Reference - Core (DRF)

**Base URL**: `http://localhost:8000/api/`

### Authentication

The API uses JWT (JSON Web Token) authentication with the following endpoints:

#### Login
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### JWT Token Login
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### Refresh Token
```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token"}'
```

#### Get User Profile
```bash
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer your_access_token"
```

#### Change Password
```bash
curl -X POST http://localhost:8000/api/users/change_password/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"old_password": "admin123", "new_password": "newpassword123"}'
```

#### Logout
```bash
curl -X POST http://localhost:8000/api/users/logout/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "your_refresh_token"}'
```

### Users API

**Endpoint**: `/api/users/`

#### List Users
```bash
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Bearer your_access_token"
```

#### Create User (SuperAdmin only)
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newfarmer",
    "email": "farmer@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "FARMER",
    "phone_number": "+1234567890"
  }'
```

### Farms API

**Endpoint**: `/api/farms/`

#### List Farms
```bash
curl -X GET http://localhost:8000/api/farms/ \
  -H "Authorization: Bearer your_access_token"
```

#### Create Farm (SuperAdmin/Agent only)
```bash
curl -X POST http://localhost:8000/api/farms/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sunset Dairy Farm",
    "agent": 2,
    "location": "123 Sunset Road, Dairy County",
    "size_acres": 200.0,
    "description": "Modern dairy farm with automated milking"
  }'
```

### Cows API

**Endpoint**: `/api/cows/`

#### List Cows
```bash
curl -X GET http://localhost:8000/api/cows/ \
  -H "Authorization: Bearer your_access_token"
```

#### Create Cow (Farmer only)
```bash
curl -X POST http://localhost:8000/api/cows/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "tag_number": "COW003",
    "name": "Rosie",
    "breed": "HOLSTEIN",
    "farmer": 3,
    "farm": 1,
    "date_of_birth": "2021-05-15",
    "weight_kg": 600.0,
    "height_cm": 140.0
  }'
```

### Milk Records API

**Endpoint**: `/api/milk-records/`

#### List Milk Records
```bash
curl -X GET http://localhost:8000/api/milk-records/ \
  -H "Authorization: Bearer your_access_token"
```

#### Create Milk Record (Farmer only)
```bash
curl -X POST http://localhost:8000/api/milk-records/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "cow": 1,
    "farmer": 3,
    "farm": 1,
    "date": "2024-01-20",
    "morning_quantity_liters": 12.5,
    "evening_quantity_liters": 11.8,
    "fat_percentage": 3.85,
    "protein_percentage": 3.20,
    "quality_rating": "EXCELLENT"
  }'
```

### Activities API

**Endpoint**: `/api/activities/`

#### List Activities
```bash
curl -X GET http://localhost:8000/api/activities/ \
  -H "Authorization: Bearer your_access_token"
```

#### Create Activity (Farmer only)
```bash
curl -X POST http://localhost:8000/api/activities/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Vaccination - Bessie",
    "activity_type": "VACCINATION",
    "cow": 1,
    "scheduled_date": "2024-02-01",
    "scheduled_time": "09:00:00",
    "description": "Annual vaccination schedule"
  }'
```

## API Reference - Reporting (FastAPI)

**Base URL**: `http://localhost:8001/`

The FastAPI reporting service provides read-only endpoints with automatic API documentation at `http://localhost:8001/docs`.

### Health Check
```bash
curl -X GET http://localhost:8001/health
```

### Production Summary
```bash
curl -X GET "http://localhost:8001/reports/production-summary?from_date=2024-01-01&to_date=2024-01-31"
```

### Farm Summary
```bash
curl -X GET "http://localhost:8001/reports/farm-summary?farm_id=1"
```

### Activity Summary
```bash
curl -X GET "http://localhost:8001/reports/activity-summary?activity_type=VACCINATION"
```

### Milk Production Filtered
```bash
curl -X GET "http://localhost:8001/reports/milk-production?farm_id=1&from_date=2024-01-01&limit=50"
```

### Recent Activities
```bash
curl -X GET "http://localhost:8001/reports/recent-activities?days=7&activity_type=VACCINATION"
```

### Users (Read-only)
```bash
curl -X GET "http://localhost:8001/users?role=FARMER&limit=10"
```

### Farms (Read-only)
```bash
curl -X GET "http://localhost:8001/farms?is_active=true"
```

### Cows (Read-only)
```bash
curl -X GET "http://localhost:8001/cows?breed=HOLSTEIN&farm_id=1"
```

### Milk Records (Read-only)
```bash
curl -X GET "http://localhost:8001/milk-records?cow_id=1&from_date=2024-01-01&to_date=2024-01-31"
```

### Activities (Read-only)
```bash
curl -X GET "http://localhost:8001/activities?cow_id=1&activity_type=VACCINATION&status=COMPLETED"
```

## Postman Collection

**Status**: Exported Postman collection pending.

A comprehensive Postman collection will be provided for testing all API endpoints with pre-configured authentication and sample request bodies.

## Docker/Compose

**Status**: Not Yet Implemented

Docker and Docker Compose configuration files are not present in the repository. This is marked as optional for the assignment.

## Deployment Notes

The project includes Render deployment configuration in `render.yaml`:

### Render Deployment
- **Django API**: `farmhub-django-api` service
- **FastAPI Reporting**: `farmhub-fastapi-reporting` service
- **Database**: PostgreSQL on Render
- **Build Commands**: Automated setup with migrations and seed data
- **Environment**: Production-ready with proper security settings

### Deployment Commands
```bash
# Django Core Service
cd core && pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python manage.py setup_deployment
cd core && gunicorn core_service.wsgi:application

# FastAPI Reporting Service
cd reporting && pip install -r requirements-render.txt
cd reporting && python start_simple_render.py
```

## Troubleshooting

### Common Issues

#### Migration Errors
```bash
# Reset migrations if needed
cd core
python manage.py makemigrations --empty users farms cows milk activities
python manage.py migrate
```

#### Environment Variables
- Ensure `.env` file exists in root directory
- Check `DEBUG` setting for development vs production
- Verify `DATABASE_URL` format for PostgreSQL

#### Port Conflicts
- Django Core: Default port 8000
- FastAPI Reporting: Default port 8001
- Change ports in run commands if conflicts occur

#### CORS Issues
- FastAPI CORS is configured to allow all origins in development
- Configure properly for production deployment

#### Database Connection
- Local development uses SQLite by default
- Production uses PostgreSQL via `DATABASE_URL`
- Ensure database is accessible and credentials are correct

### Development Tips

1. **Virtual Environment**: Always activate virtual environment before running services
2. **Requirements**: Install requirements for both core and reporting services
3. **Migrations**: Run migrations after any model changes
4. **Seed Data**: Load seed data for testing with sample data
5. **Logs**: Check console output for detailed error messages

---

For detailed API documentation, visit:
- Django API: `http://localhost:8000/api/`
- Django Admin: `http://localhost:8000/admin/`
- Reporting API: `http://localhost:8001/docs`
