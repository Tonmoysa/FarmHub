from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from farms.models import Farm
from cows.models import Cow
from milk.models import MilkRecord
from activities.models import Activity
from datetime import date, datetime, timedelta
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Adds initial seed data for FarmHub system'

    def handle(self, *args, **options):
        self.stdout.write('Creating seed data...')
        
        # Create Agent
        agent = User.objects.create_user(
            username='agent1',
            email='agent1@farmhub.com',
            password='agent123',
            first_name='John',
            last_name='Agent',
            role='AGENT',
            phone_number='+1234567891',
            address='123 Agent Street, Farm City',
            date_of_birth=date(1985, 5, 15)
        )
        self.stdout.write(f'Created Agent: {agent.username}')
        
        # Create Farm
        farm = Farm.objects.create(
            name='Green Valley Farm',
            agent=agent,
            location='456 Farm Road, Green Valley',
            size_acres=Decimal('150.50'),
            description='A beautiful dairy farm in the green valley with modern facilities.',
            is_active=True
        )
        self.stdout.write(f'Created Farm: {farm.name}')
        
        # Create Farmer
        farmer = User.objects.create_user(
            username='farmer1',
            email='farmer1@farmhub.com',
            password='farmer123',
            first_name='Sarah',
            last_name='Farmer',
            role='FARMER',
            phone_number='+1234567892',
            address='789 Farmer Lane, Green Valley',
            date_of_birth=date(1990, 8, 20)
        )
        self.stdout.write(f'Created Farmer: {farmer.username}')
        
        # Create Cows
        cow1 = Cow.objects.create(
            tag_number='COW001',
            name='Bessie',
            breed='HOLSTEIN',
            farmer=farmer,
            farm=farm,
            date_of_birth=date(2020, 3, 15),
            weight_kg=Decimal('650.00'),
            height_cm=Decimal('145.00'),
            status='ACTIVE',
            is_pregnant=False
        )
        self.stdout.write(f'Created Cow: {cow1.tag_number} - {cow1.name}')
        
        cow2 = Cow.objects.create(
            tag_number='COW002',
            name='Daisy',
            breed='JERSEY',
            farmer=farmer,
            farm=farm,
            date_of_birth=date(2019, 7, 22),
            weight_kg=Decimal('450.00'),
            height_cm=Decimal('130.00'),
            status='ACTIVE',
            is_pregnant=True,
            last_breeding_date=date(2024, 1, 15)
        )
        self.stdout.write(f'Created Cow: {cow2.tag_number} - {cow2.name}')
        
        # Create Milk Records
        today = date.today()
        
        # Milk records for the last 7 days
        for i in range(7):
            record_date = today - timedelta(days=i)
            
            # Record for Cow 1
            MilkRecord.objects.create(
                cow=cow1,
                farmer=farmer,
                farm=farm,
                date=record_date,
                morning_quantity_liters=Decimal('12.50'),
                evening_quantity_liters=Decimal('11.80'),
                fat_percentage=Decimal('3.80'),
                protein_percentage=Decimal('3.20'),
                quality_rating='EXCELLENT',
                notes=f'Good production day for {cow1.name}'
            )
            
            # Record for Cow 2
            MilkRecord.objects.create(
                cow=cow2,
                farmer=farmer,
                farm=farm,
                date=record_date,
                morning_quantity_liters=Decimal('8.20'),
                evening_quantity_liters=Decimal('7.90'),
                fat_percentage=Decimal('4.50'),
                protein_percentage=Decimal('3.80'),
                quality_rating='EXCELLENT',
                notes=f'High fat content from {cow2.name}'
            )
        
        self.stdout.write('Created 14 milk records (7 days for 2 cows)')
        
        # Create Activities
        activities_data = [
            {
                'title': 'Morning Milking',
                'activity_type': 'MILKING',
                'cow': cow1,
                'scheduled_date': today,
                'scheduled_time': datetime.strptime('06:00', '%H:%M').time(),
                'status': 'COMPLETED',
                'description': 'Regular morning milking session',
                'cost': Decimal('0.00')
            },
            {
                'title': 'Health Check',
                'activity_type': 'HEALTH_CHECK',
                'cow': cow2,
                'scheduled_date': today + timedelta(days=1),
                'scheduled_time': datetime.strptime('10:00', '%H:%M').time(),
                'status': 'PLANNED',
                'description': 'Routine health check for pregnant cow',
                'cost': Decimal('50.00')
            },
            {
                'title': 'Feeding Session',
                'activity_type': 'FEEDING',
                'cow': cow1,
                'scheduled_date': today,
                'scheduled_time': datetime.strptime('12:00', '%H:%M').time(),
                'status': 'COMPLETED',
                'description': 'Afternoon feeding with balanced nutrition',
                'cost': Decimal('25.00')
            },
            {
                'title': 'Vaccination',
                'activity_type': 'VACCINATION',
                'cow': cow1,
                'scheduled_date': today + timedelta(days=3),
                'scheduled_time': datetime.strptime('14:00', '%H:%M').time(),
                'status': 'PLANNED',
                'description': 'Annual vaccination schedule',
                'cost': Decimal('75.00')
            },
            {
                'title': 'Evening Milking',
                'activity_type': 'MILKING',
                'cow': cow2,
                'scheduled_date': today,
                'scheduled_time': datetime.strptime('18:00', '%H:%M').time(),
                'status': 'COMPLETED',
                'description': 'Regular evening milking session',
                'cost': Decimal('0.00')
            }
        ]
        
        for activity_data in activities_data:
            Activity.objects.create(**activity_data)
        
        self.stdout.write('Created 5 activities')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created all seed data!')
        )
        self.stdout.write('\nSummary:')
        self.stdout.write('- 1 Agent (agent1/agent123)')
        self.stdout.write('- 1 Farm (Green Valley Farm)')
        self.stdout.write('- 1 Farmer (farmer1/farmer123)')
        self.stdout.write('- 2 Cows (COW001-Bessie, COW002-Daisy)')
        self.stdout.write('- 14 Milk Records (7 days for each cow)')
        self.stdout.write('- 5 Activities (milking, health check, feeding, vaccination)')
