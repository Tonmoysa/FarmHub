from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser with default credentials for immediate access'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@farmhub.com'
        password = 'admin123'
        
        # Check if superuser already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists.')
            )
            
            # Try to reset password
            try:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Password reset for superuser "{username}"')
                )
                self.stdout.write(f'Username: {username}')
                self.stdout.write(f'Password: {password}')
                self.stdout.write(f'Email: {email}')
                return
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error resetting password: {e}')
                )
                return
        
        try:
            # Create superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Super',
                last_name='Admin',
                role='SUPER_ADMIN',
                phone_number='+1234567890',
                address='FarmHub Headquarters',
                date_of_birth=date(1990, 1, 1)
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Successfully created superuser "{username}"')
            )
            self.stdout.write(f'Username: {username}')
            self.stdout.write(f'Password: {password}')
            self.stdout.write(f'Email: {email}')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating superuser: {e}')
            )
            self.stdout.write('Trying alternative method...')
            
            try:
                # Alternative method using direct user creation
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name='Super',
                    last_name='Admin',
                    role='SUPER_ADMIN',
                    phone_number='+1234567890',
                    address='FarmHub Headquarters',
                    date_of_birth=date(1990, 1, 1),
                    is_staff=True,
                    is_superuser=True,
                    is_active=True
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Successfully created superuser "{username}" (alternative method)')
                )
                self.stdout.write(f'Username: {username}')
                self.stdout.write(f'Password: {password}')
                self.stdout.write(f'Email: {email}')
                
            except Exception as e2:
                self.stdout.write(
                    self.style.ERROR(f'❌ Alternative method also failed: {e2}')
                )
