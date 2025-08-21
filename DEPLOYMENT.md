# FarmHub Deployment Guide for Render

This guide will help you deploy both the Django Core Service and FastAPI Reporting Service on Render.

## 🚀 Prerequisites

1. **GitHub Repository**: Your FarmHub project should be pushed to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Database**: You'll need a PostgreSQL database (Render provides this)

## 📋 Deployment Steps

### Step 1: Create PostgreSQL Database on Render

1. Go to your Render dashboard
2. Click "New" → "PostgreSQL"
3. Configure:
   - **Name**: `farmhub-database`
   - **Database**: `farmhub_db`
   - **User**: `farmhub_user`
   - **Region**: Choose closest to your users
4. Click "Create Database"
5. **Save the connection details** - you'll need them for both services

### Step 2: Deploy Django Core Service

1. In Render dashboard, click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure the service:

#### Basic Settings:
- **Name**: `farmhub-core`
- **Environment**: `Python 3`
- **Region**: Same as database
- **Branch**: `main`
- **Root Directory**: `core`

#### Build & Deploy Settings:
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn core_service.wsgi:application`

#### Environment Variables:
```
DATABASE_URL=postgresql://farmhub_user:password@host:port/farmhub_db
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

### Step 3: Deploy FastAPI Reporting Service

1. In Render dashboard, click "New" → "Web Service"
2. Connect your GitHub repository (same repo)
3. Configure the service:

#### Basic Settings:
- **Name**: `farmhub-reporting`
- **Environment**: `Python 3`
- **Region**: Same as database
- **Branch**: `main`
- **Root Directory**: `reporting`

#### Build & Deploy Settings:
- **Build Command**: `./build.sh`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Environment Variables:
```
DATABASE_URL=postgresql://farmhub_user:password@host:port/farmhub_db
```

## 🔧 Environment Variables

### Django Core Service Required Variables:
```bash
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-very-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

### FastAPI Reporting Service Required Variables:
```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

## 📊 Service URLs

After deployment, your services will be available at:
- **Django Core**: `https://farmhub-core.onrender.com`
- **FastAPI Reporting**: `https://farmhub-reporting.onrender.com`
- **API Documentation**: `https://farmhub-reporting.onrender.com/docs`

## 🔄 Database Migration

After the first deployment:

1. Go to your Django service dashboard on Render
2. Click "Shell"
3. Run these commands:
```bash
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py createsuperuser
```

## 🛡️ Security Considerations

1. **Secret Key**: Generate a secure secret key:
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

2. **Environment Variables**: Never commit sensitive data to Git

3. **CORS**: Update CORS settings in production:
   ```python
   CORS_ALLOWED_ORIGINS = [
       "https://your-frontend-domain.com",
   ]
   ```

## 🔍 Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check build logs in Render dashboard
   - Ensure all requirements are in requirements.txt
   - Verify build.sh has execute permissions

2. **Database Connection**:
   - Verify DATABASE_URL format
   - Check if database is accessible from your region
   - Ensure database user has proper permissions

3. **Static Files**:
   - Django will automatically collect static files during build
   - WhiteNoise handles static file serving

4. **Port Issues**:
   - Render automatically sets PORT environment variable
   - Use `$PORT` in start commands

## 📈 Monitoring

- **Health Checks**: Both services have `/health` endpoints
- **Logs**: View real-time logs in Render dashboard
- **Metrics**: Monitor performance in Render dashboard

## 🔄 Updates

To update your deployment:
1. Push changes to your GitHub repository
2. Render will automatically detect changes and redeploy
3. Monitor build logs for any issues

## 📞 Support

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Django Deployment**: [docs.djangoproject.com/en/stable/howto/deployment/](https://docs.djangoproject.com/en/stable/howto/deployment/)
- **FastAPI Deployment**: [fastapi.tiangolo.com/deployment/](https://fastapi.tiangolo.com/deployment/)
