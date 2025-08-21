# FarmHub - Farm Management Platform

A simplified farm management platform designed for an agritech company. FarmHub allows registration of farms, onboarding of farmers, enrollment of cows, and tracking of daily operations such as milk production and health-related activities.

## 🎯 Project Overview

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

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- pip package manager

### 1. Clone and Setup
```bash
git clone <repository-url>
cd FarmHub
```

### 2. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
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

## 👥 Role Design & Permissions

The platform has three primary roles with proper role-based access control:

### 1. SuperAdmin
- **Role**: System administrator with full access
- **Permissions**: 
  - Create, edit, and delete all users (Agents, Farmers)
  - Create and manage all farms
  - View and audit all data across the platform
  - Assign Agents to farms
- **Responsibilities**: System-wide oversight and user management

### 2. Agent
- **Role**: Farm management coordinator
- **Permissions**: 
  - Manage assigned farms only
  - Onboard farmers to their assigned farms
  - Record and manage farm-level data
  - View data within their scope of assigned farms
- **Responsibilities**: Farm oversight, farmer coordination, regional management

### 3. Farmer
- **Role**: Individual farm operator
- **Permissions**: 
  - Belong to a single farm
  - Manage their own cows
  - Record daily milk production
  - Log activities (vaccinations, births, health checks)
- **Responsibilities**: Daily operations, milk recording, livestock care

## 🗄️ Database & Data Model

### Core Entities

#### Farm
- **Fields**: Name, location, size, agent assignment, status
- **Relationships**: Managed by Agent, contains Cows, produces Milk Records

#### Cow
- **Fields**: Tag number, name, breed, birth date, weight, height, status
- **Relationships**: Owned by Farmer, located at Farm, produces Milk Records

#### Milk Record
- **Fields**: Date, morning/evening quantities, fat/protein percentages, quality rating
- **Relationships**: Produced by Cow, recorded by Farmer, associated with Farm

#### Activity
- **Fields**: Type, scheduled date, status, description, cost
- **Relationships**: Associated with Cow, tracked by Farmer

## 🔌 API Examples

### Authentication
```bash
# Custom Login (with user details)
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# JWT Token Login
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Refresh Token
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token"}'

# Get User Profile
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer your_access_token"

# Change Password
curl -X POST http://localhost:8000/api/users/change_password/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"old_password": "admin123", "new_password": "newpassword123"}'

# Logout
curl -X POST http://localhost:8000/api/users/logout/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "your_refresh_token"}'
```

### Farm Management
```bash
# Create new farm (SuperAdmin/Agent only)
curl -X POST http://localhost:8000/api/farms/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sunset Dairy Farm",
    "location": "123 Sunset Road, Dairy County",
    "size_acres": 200.0,
    "description": "Modern dairy farm with automated milking"
  }'

# List farms
curl -X GET http://localhost:8000/api/farms/ \
  -H "Authorization: Bearer <token>"
```

### Cow Registration
```bash
# Register new cow (Farmer only)
curl -X POST http://localhost:8000/api/cows/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "tag_number": "COW003",
    "name": "Rosie",
    "breed": "HOLSTEIN",
    "date_of_birth": "2021-05-15",
    "weight_kg": 600.0,
    "height_cm": 140.0
  }'

# List cows
curl -X GET http://localhost:8000/api/cows/ \
  -H "Authorization: Bearer <token>"
```

### Milk Production Entry
```bash
# Record milk production (Farmer only)
curl -X POST http://localhost:8000/api/milk-records/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "cow": 1,
    "date": "2024-01-20",
    "morning_quantity_liters": 12.5,
    "evening_quantity_liters": 11.8,
    "fat_percentage": 3.85,
    "protein_percentage": 3.20,
    "quality_rating": "EXCELLENT"
  }'
```

### Activity Management
```bash
# Schedule activity (Farmer only)
curl -X POST http://localhost:8000/api/activities/ \
  -H "Authorization: Bearer <token>" \
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

### Reporting API (FastAPI Service)
```bash
# Production summary
curl -X GET "http://localhost:8001/reports/production-summary?from_date=2024-01-01&to_date=2024-01-31"

# Farm summary
curl -X GET "http://localhost:8001/reports/farm-summary?farm_id=1"

# Activity summary
curl -X GET "http://localhost:8001/reports/activity-summary?activity_type=VACCINATION"

# Milk production filtering
curl -X GET "http://localhost:8001/milk-records?farm_id=1&from_date=2024-01-01&limit=50"
```

## 🌱 Seed Data Information

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

## 📊 Reporting Service

The FastAPI reporting service provides read-only, aggregated reports including:
- Farm summary showing number of farmers, cows, and total milk production
- Milk production filtered by farm, farmer, or date range
- Summaries of recent activities
- Production summaries and trends
- API documentation at `http://localhost:8001/docs`

## 🛠️ Development

### Technology Stack
- **Backend**: Django + Django REST Framework
- **Reporting**: FastAPI + SQLAlchemy
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Django REST Framework tokens

### Project Structure
```
FarmHub/
├── core/                    # Django core service
│   ├── users/              # User management
│   ├── farms/              # Farm management
│   ├── cows/               # Livestock management
│   ├── milk/               # Milk production
│   ├── activities/         # Activity tracking
│   ├── fixtures/           # Seed data
│   └── core_service/       # Django settings
├── reporting/              # FastAPI reporting service
│   ├── main.py            # FastAPI application
│   ├── models.py          # Database models
│   └── schemas.py         # Pydantic schemas
└── venv/                  # Virtual environment
```

## 🔒 Security Notes

- All passwords are properly hashed using Django's password hasher
- API endpoints require authentication via tokens
- Role-based access control implemented
- Reporting service is read-only for data safety

## 📦 Postman Collection

A comprehensive Postman collection is included with this project:
- **File**: `FarmHub_API_Collection.json`
- **Features**: 
  - Complete authentication endpoints
  - All CRUD operations for Users, Farms, Cows, Milk Records, Activities
  - Reporting service endpoints
  - Pre-configured variables for easy testing
  - Sample request bodies for all endpoints

### Import Instructions:
1. Open Postman
2. Click "Import" button
3. Select `FarmHub_API_Collection.json`
4. Set environment variables:
   - `base_url`: `http://localhost:8000`
   - `reporting_url`: `http://localhost:8001`
   - `access_token`: (will be set after login)
   - `refresh_token`: (will be set after login)

## 📝 License

This project is proprietary software for farm management systems.

---

For detailed API documentation, visit:
- Django API: `http://localhost:8000/api/`
- Reporting API: `http://localhost:8001/docs`
- Postman Collection: `FarmHub_API_Collection.json`
