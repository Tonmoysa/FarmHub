# FarmHub Reporting Service

A FastAPI-based read-only reporting and analytics service for the FarmHub system. This service connects to the Django core database to provide real-time reporting and data visualization capabilities.

## Features

- **Read-only Access**: Safe reporting service that doesn't modify core data
- **RESTful API**: FastAPI-based endpoints with automatic documentation
- **Real-time Data**: Direct connection to Django database for live data
- **Comprehensive Reports**: Production, activity, health, and financial reporting
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## API Endpoints

### Core Data Endpoints
- `GET /users` - List users with filtering
- `GET /farms` - List farms with filtering  
- `GET /cows` - List cows with filtering
- `GET /milk-records` - List milk records with filtering
- `GET /activities` - List activities with filtering

### Reporting Endpoints
- `GET /reports/production-summary` - Milk production summary
- `GET /reports/activity-summary` - Activity summary
- `GET /health` - Service health check
- `GET /docs` - API documentation (Swagger UI)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the service:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## Configuration

The service is configured to:
- Connect to the Django SQLite database at `../core/db.sqlite3`
- Run on port 8001 (Django runs on 8000)
- Provide read-only access to prevent data corruption
- Include CORS middleware for web client access

## Database Connection

The service uses SQLAlchemy to connect to the same SQLite database used by Django. The models in `models.py` mirror the Django models but are read-only.

## API Documentation

Once the service is running, visit:
- `http://localhost:8001/docs` - Swagger UI documentation
- `http://localhost:8001/redoc` - ReDoc documentation

## Usage Examples

### Get Production Summary
```bash
curl "http://localhost:8001/reports/production-summary?from_date=2024-01-01&to_date=2024-01-31"
```

### Get Milk Records for a Farm
```bash
curl "http://localhost:8001/milk-records?farm_id=1&limit=50"
```

### Get Activity Summary
```bash
curl "http://localhost:8001/reports/activity-summary?activity_type=VACCINATION"
```

## Development

The service is built with:
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: Database ORM for model definitions
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for development and production

## Security Notes

- This is a read-only service - no write operations are supported
- All database connections are read-only
- CORS is configured for development (adjust for production)
- No authentication is implemented (add as needed for production)
