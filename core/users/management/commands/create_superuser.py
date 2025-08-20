from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser with predefined credentials'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@farmhub.com'
        password = 'admin123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists.')
            )
            return
        
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
            self.style.SUCCESS(f'Successfully created superuser "{username}"')
        )
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write(f'Email: {email}')
