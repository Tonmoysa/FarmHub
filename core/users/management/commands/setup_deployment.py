from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import transaction
from django.conf import settings
import os
import json
from pathlib import Path

User = get_user_model()

class Command(BaseCommand):
    help = 'Sets up deployment with initial data and superuser creation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reload data even if it exists',
        )
        parser.add_argument(
            '--skip-superuser',
            action='store_true',
            help='Skip superuser creation',
        )
        parser.add_argument(
            '--skip-fixtures',
            action='store_true',
            help='Skip loading fixtures',
        )

    def handle(self, *args, **options):
        self.stdout.write('🚀 Starting deployment setup...')
        
        # Check if this is a fresh deployment
        is_fresh_deployment = self._is_fresh_deployment()
        
        if is_fresh_deployment:
            self.stdout.write('📦 Fresh deployment detected')
        else:
            self.stdout.write('🔄 Existing deployment detected')
        
        # Create superuser if needed
        if not options['skip_superuser']:
            self._create_superuser()
        
        # Load initial data if needed
        if not options['skip_fixtures']:
            self._load_initial_data(force=options['force'])
        
        self.stdout.write('✅ Deployment setup completed successfully!')

    def _is_fresh_deployment(self):
        """Check if this is a fresh deployment by looking for existing data"""
        try:
            # Check if any users exist
            user_count = User.objects.count()
            if user_count == 0:
                return True
            
            # Check if admin user exists
            admin_exists = User.objects.filter(username='admin').exists()
            if not admin_exists:
                return True
                
            return False
        except Exception as e:
            self.stdout.write(f'⚠️  Error checking deployment status: {e}')
            return True

    def _create_superuser(self):
        """Create superuser if it doesn't exist"""
        self.stdout.write('👤 Setting up superuser...')
        
        try:
            # Check if superuser already exists
            if User.objects.filter(username='admin').exists():
                self.stdout.write(
                    self.style.WARNING('Superuser "admin" already exists. Skipping creation.')
                )
                return
            
            # Create superuser using environment variables or defaults
            username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@farmhub.com')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
            
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Super',
                last_name='Admin',
                role='SUPER_ADMIN',
                phone_number='+1234567890',
                address='FarmHub Headquarters',
                date_of_birth='1990-01-01'
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Successfully created superuser "{username}"')
            )
            self.stdout.write(f'   Username: {username}')
            self.stdout.write(f'   Email: {email}')
            self.stdout.write(f'   Password: {password}')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating superuser: {e}')
            )

    def _load_initial_data(self, force=False):
        """Load initial data from fixtures"""
        self.stdout.write('📊 Loading initial data...')
        
        try:
            # Check if data already exists
            if not force and self._data_exists():
                self.stdout.write(
                    self.style.WARNING('Initial data already exists. Skipping load.')
                )
                return
            
            # Load fixtures
            fixture_path = Path(settings.BASE_DIR) / 'fixtures' / 'initial_data.json'
            
            if not fixture_path.exists():
                self.stdout.write(
                    self.style.WARNING(f'Fixture file not found: {fixture_path}')
                )
                return
            
            # Load the fixture
            with transaction.atomic():
                call_command('loaddata', str(fixture_path), verbosity=0)
            
            self.stdout.write(
                self.style.SUCCESS('✅ Successfully loaded initial data')
            )
            
            # Display loaded data summary
            self._display_data_summary()
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error loading initial data: {e}')
            )

    def _data_exists(self):
        """Check if initial data already exists"""
        try:
            # Check for key data that should exist after loading fixtures
            user_count = User.objects.count()
            from farms.models import Farm
            from cows.models import Cow
            
            farm_count = Farm.objects.count()
            cow_count = Cow.objects.count()
            
            # If we have users, farms, and cows, assume data is loaded
            return user_count > 1 and farm_count > 0 and cow_count > 0
            
        except Exception:
            return False

    def _display_data_summary(self):
        """Display a summary of loaded data"""
        try:
            user_count = User.objects.count()
            from farms.models import Farm
            from cows.models import Cow
            from milk.models import MilkRecord
            from activities.models import Activity
            
            farm_count = Farm.objects.count()
            cow_count = Cow.objects.count()
            milk_count = MilkRecord.objects.count()
            activity_count = Activity.objects.count()
            
            self.stdout.write('\n📈 Data Summary:')
            self.stdout.write(f'   Users: {user_count}')
            self.stdout.write(f'   Farms: {farm_count}')
            self.stdout.write(f'   Cows: {cow_count}')
            self.stdout.write(f'   Milk Records: {milk_count}')
            self.stdout.write(f'   Activities: {activity_count}')
            
        except Exception as e:
            self.stdout.write(f'⚠️  Error displaying data summary: {e}')
