# FarmHub Initial Data Fixture

This directory contains the `initial_data.json` fixture file with sample seed data for the FarmHub project.

## Contents

The fixture includes:

### Users
1. **SuperAdmin** (username: `admin`, password: `admin123`)
   - Email: admin@example.com
   - Role: SUPER_ADMIN
   - Full access to all system features

2. **Agent** (username: `agent1`, password: `agent123`)
   - Email: agent1@example.com
   - Role: AGENT
   - Manages Green Valley Farm

3. **Farmer** (username: `farmer1`, password: `farmer123`)
   - Email: farmer1@example.com
   - Role: FARMER
   - Owns cows and records milk production

### Farm
- **Green Valley Farm**: 150-acre dairy farm managed by agent1

### Cows
- **COW001 (Bessie)**: Holstein breed, owned by farmer1
- **COW002 (Daisy)**: Jersey breed, pregnant, owned by farmer1

### Milk Records
- 3 milk production records across different dates
- Includes quality metrics (fat %, protein %)
- Linked to specific cows and farmer

### Activities
- Vaccination activity for Bessie (completed)
- Health check for Daisy (completed)
- Scheduled maintenance activity (planned)

## Usage

### For Fresh Installation
```bash
# Navigate to the core directory
cd core

# Activate virtual environment
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Load the fixture
python manage.py loaddata fixtures/initial_data.json
```

### For Existing Database
If you have existing data and want to avoid conflicts:

1. **Option 1: Clear database first**
   ```bash
   python manage.py flush  # This will clear all data
   python manage.py loaddata fixtures/initial_data.json
   ```

2. **Option 2: Use different usernames**
   - Edit the fixture file to change usernames
   - Or create a custom fixture with different data

3. **Option 3: Load specific models**
   ```bash
   # Load only farms (if no farms exist)
   python manage.py loaddata fixtures/initial_data.json --app farms
   
   # Load only cows (if no cows exist)
   python manage.py loaddata fixtures/initial_data.json --app cows
   ```

## Login Credentials

After loading the fixture, you can log in with:

- **Admin**: username=`admin`, password=`admin123`
- **Agent**: username=`agent1`, password=`agent123`
- **Farmer**: username=`farmer1`, password=`farmer123`

## Notes

- All passwords are properly hashed using Django's password hasher
- All relationships use correct primary key references
- The fixture follows Django's JSON fixture format
- Timestamps are set to reasonable dates for testing
- The data is realistic and suitable for development/testing

## Customization

You can modify the fixture file to:
- Add more users, farms, cows, or activities
- Change passwords (remember to hash them properly)
- Adjust dates, quantities, or other data
- Add more milk records or activities

To generate new password hashes:
```python
from django.contrib.auth.hashers import make_password
print(make_password('your_password'))
```
