# Core Service

Django-based core service for FarmHub farm management system.

## Apps

- **users**: User management and authentication
- **farms**: Farm management and configuration
- **cows**: Cow inventory and management
- **milk**: Milk production tracking
- **activities**: Farm activities and events

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Run development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

The service provides REST API endpoints for all farm management operations.

## Development

- Django 5.2.5
- Django REST Framework 3.15.0
- SQLite database (development)
