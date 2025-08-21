# FarmHub Deployment Guide

This guide explains the automated deployment process for FarmHub, including initial data loading and superuser creation.

## 🚀 Automated Deployment Features

### 1. Initial Data Loading
- **Automatic**: Loads `initial_data.json` fixture during deployment
- **Smart Detection**: Only loads data if it doesn't already exist
- **Duplicate Prevention**: Prevents duplicate data loading
- **Transaction Safety**: Uses database transactions for data integrity

### 2. Superuser Creation
- **Automatic**: Creates admin superuser during deployment
- **Environment Variables**: Configurable via environment variables
- **Duplicate Prevention**: Only creates if superuser doesn't exist
- **Secure**: Uses proper password hashing

## 📁 Project Structure

```
FarmHub/
├── core/
│   ├── fixtures/
│   │   ├── initial_data.json      # Initial seed data
│   │   └── README.md              # Fixture documentation
│   ├── users/management/commands/
│   │   ├── setup_deployment.py    # Main deployment command
│   │   ├── create_superuser.py    # Superuser creation
│   │   └── seed_data.py           # Manual data seeding
│   ├── build.sh                   # Build script
│   └── requirements.txt           # Dependencies
├── reporting/                     # FastAPI service
├── render.yaml                    # Render deployment config
└── runtime.txt                    # Python version
```

## 🔧 Management Commands

### Setup Deployment Command
```bash
python manage.py setup_deployment
```

**Options:**
- `--force`: Force reload data even if it exists
- `--skip-superuser`: Skip superuser creation
- `--skip-fixtures`: Skip loading fixtures

**Examples:**
```bash
# Full setup (default)
python manage.py setup_deployment

# Force reload all data
python manage.py setup_deployment --force

# Only create superuser, skip fixtures
python manage.py setup_deployment --skip-fixtures

# Only load fixtures, skip superuser
python manage.py setup_deployment --skip-superuser
```

### Manual Commands
```bash
# Create superuser only
python manage.py create_superuser

# Load seed data only
python manage.py seed_data

# Load fixtures manually
python manage.py loaddata fixtures/initial_data.json
```

## 🌍 Environment Variables

### Superuser Configuration
```bash
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@farmhub.com
DJANGO_SUPERUSER_PASSWORD=admin123
```

### Database Configuration
```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

## 🏗️ Build Process

### Render Deployment
The build process automatically:

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Collect Static Files**
   ```bash
   python manage.py collectstatic --no-input
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Setup Deployment**
   ```bash
   python manage.py setup_deployment
   ```

### Local Development
```bash
# Navigate to core directory
cd core

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Setup deployment (optional)
python manage.py setup_deployment
```

## 📊 Initial Data

### What Gets Loaded
- **Users**: Admin, Agent, Farmer accounts
- **Farms**: Sample farm data
- **Cows**: Sample cow records
- **Milk Records**: Historical milk production data
- **Activities**: Sample farm activities

### Login Credentials
After deployment, you can log in with:

| Role | Username | Password | Email |
|------|----------|----------|-------|
| Super Admin | admin | admin123 | admin@farmhub.com |
| Agent | agent1 | agent123 | agent1@example.com |
| Farmer | farmer1 | farmer123 | farmer1@example.com |

## 🔒 Security Features

### Duplicate Prevention
- **Smart Detection**: Checks existing data before loading
- **User Existence**: Prevents duplicate superuser creation
- **Data Integrity**: Uses database transactions
- **Safe Reloads**: Can force reload with `--force` flag

### Environment Variables
- **Configurable**: All sensitive data via environment variables
- **Secure**: Passwords not hardcoded
- **Flexible**: Different values for different environments

## 🐛 Troubleshooting

### Common Issues

1. **Fixture Loading Fails**
   ```bash
   # Check fixture path
   ls core/fixtures/initial_data.json
   
   # Manual load with verbose output
   python manage.py loaddata fixtures/initial_data.json --verbosity=2
   ```

2. **Superuser Creation Fails**
   ```bash
   # Check if user exists
   python manage.py shell
   >>> from django.contrib.auth import get_user_model
   >>> User = get_user_model()
   >>> User.objects.filter(username='admin').exists()
   ```

3. **Database Connection Issues**
   ```bash
   # Test database connection
   python manage.py dbshell
   
   # Check migrations
   python manage.py showmigrations
   ```

### Debug Commands
```bash
# Check deployment status
python manage.py setup_deployment --verbosity=2

# Force reload everything
python manage.py setup_deployment --force

# Check data summary
python manage.py shell
>>> from users.management.commands.setup_deployment import Command
>>> cmd = Command()
>>> cmd._display_data_summary()
```

## 📈 Monitoring

### Deployment Logs
Monitor these log messages during deployment:

```
🚀 Starting deployment setup...
📦 Fresh deployment detected
👤 Setting up superuser...
✅ Successfully created superuser "admin"
📊 Loading initial data...
✅ Successfully loaded initial data
📈 Data Summary:
   Users: 3
   Farms: 1
   Cows: 2
   Milk Records: 7
   Activities: 3
✅ Deployment setup completed successfully!
```

### Health Checks
After deployment, verify:

1. **Database Connection**: Check if migrations ran successfully
2. **Superuser Access**: Try logging in with admin credentials
3. **Data Loading**: Check if sample data exists
4. **API Endpoints**: Test API functionality

## 🔄 Database Support

### PostgreSQL (Production)
- **Render**: Automatic setup with PostgreSQL
- **SSL**: Required for Render connections
- **Connection Pooling**: Optimized for production

### SQLite (Development)
- **Local**: Default for development
- **File-based**: No server setup required
- **Testing**: Perfect for local testing

## 📝 Customization

### Adding New Data
1. **Edit Fixture**: Modify `core/fixtures/initial_data.json`
2. **Add Models**: Include new model data in fixture
3. **Update Command**: Modify `setup_deployment.py` if needed

### Custom Superuser
```bash
# Set environment variables
export DJANGO_SUPERUSER_USERNAME=myadmin
export DJANGO_SUPERUSER_EMAIL=myadmin@example.com
export DJANGO_SUPERUSER_PASSWORD=mypassword

# Run setup
python manage.py setup_deployment
```

### Custom Build Process
Modify `build.sh` or `render.yaml` to customize the deployment process.

## 🎯 Best Practices

1. **Environment Variables**: Always use environment variables for sensitive data
2. **Idempotent**: Commands should be safe to run multiple times
3. **Error Handling**: Proper error handling and logging
4. **Testing**: Test deployment process locally before production
5. **Backup**: Always backup data before major deployments
6. **Monitoring**: Monitor deployment logs for issues

## 📞 Support

For deployment issues:
1. Check deployment logs in Render dashboard
2. Verify environment variables are set correctly
3. Test commands locally first
4. Check database connectivity
5. Review this documentation

---

**Last Updated**: January 2025
**Version**: 1.0.0
