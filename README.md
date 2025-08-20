# FarmHub - Django Core Project

This is the core Django project for FarmHub with Django REST Framework integration.

## Project Structure

```
FarmHub/
├── core/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py      # Project settings with DRF configuration
│   ├── urls.py          # Main URL configuration
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── venv/               # Python virtual environment
└── README.md           # This file
```

## Setup Instructions

1. **Activate Virtual Environment:**
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser (Optional):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run Development Server:**
   ```bash
   python manage.py runserver
   ```

## Installed Packages

- Django 5.2.5
- Django REST Framework 3.16.1

## Django REST Framework Configuration

The project is configured with the following DRF settings:

- **Authentication:** Session and Basic Authentication
- **Permissions:** IsAuthenticated (default)
- **Pagination:** PageNumberPagination with 10 items per page

## Next Steps

This is the initial project setup. The next steps would be to:
1. Create Django apps for specific functionality
2. Define models
3. Create serializers
4. Implement views and viewsets
5. Configure URL routing
