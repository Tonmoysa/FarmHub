# FarmHub Reporting Service

A FastAPI-based microservice for analytics and reporting in the FarmHub farm management platform.

## 🎯 Overview

The Reporting Service is an independent FastAPI application that provides read-only access to FarmHub data for analytics, reporting, and business intelligence. It connects directly to the Django database to provide real-time insights without affecting the core system.

### Key Features
- **Read-only Access**: Safe reporting without data modification
- **Real-time Analytics**: Live data from Django database
- **RESTful API**: FastAPI with automatic OpenAPI documentation
- **Aggregated Reports**: Production summaries, activity tracking, and farm-level analytics

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Service
```bash
# Using uvicorn directly
uvicorn main:app --host 127.0.0.1 --port 8001 --reload

# Or run the main script
python main.py
```

### 3. Verify Installation
Visit `http://127.0.0.1:8001/health` or `http://localhost:8001/health` to check service status.

## 📊 API Overview

### Core Endpoints
- `GET /` - Service information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### Data Endpoints
- `GET /users` - User data with filtering
- `GET /farms` - Farm information
- `GET /cows` - Livestock data
- `GET /milk-records` - Production records
- `GET /activities` - Activity tracking

### Reporting Endpoints
- `GET /reports/production-summary` - Milk production analytics
- `GET /reports/activity-summary` - Activity summaries
- `GET /reports/farm-summary` - Farm-level reports
- `GET /reports/milk-production` - Filtered production data
- `GET /reports/recent-activities` - Recent activity tracking

## 🔧 Configuration

The service automatically connects to the Django SQLite database at `../core/db.sqlite3`. For production, update the database connection in `database.py`.

## 📖 Documentation

- **Interactive API Docs**: `http://127.0.0.1:8001/docs` or `http://localhost:8001/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8001/redoc` or `http://localhost:8001/redoc`
- **Main FarmHub Documentation**: See root `README.md`

## 🛡️ Security

- Read-only database access
- No authentication required (add as needed for production)
- CORS enabled for web client access

---

**Note**: For complete FarmHub setup and usage instructions, refer to the main `README.md` in the project root.
