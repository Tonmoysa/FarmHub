from django.db import models
from users.models import User
from farms.models import Farm

class Cow(models.Model):
    """
    Cow model representing individual cows in the system
    """
    class Breed(models.TextChoices):
        HOLSTEIN = 'HOLSTEIN', 'Holstein'
        JERSEY = 'JERSEY', 'Jersey'
        GUERNSEY = 'GUERNSEY', 'Guernsey'
        AYRSHIRE = 'AYRSHIRE', 'Ayrshire'
        BROWN_SWISS = 'BROWN_SWISS', 'Brown Swiss'
        OTHER = 'OTHER', 'Other'
    
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        SOLD = 'SOLD', 'Sold'
        DECEASED = 'DECEASED', 'Deceased'
    
    # Basic information
    tag_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique identification tag for the cow"
    )
    
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Cow's name (optional)"
    )
    
    breed = models.CharField(
        max_length=20,
        choices=Breed.choices,
        default=Breed.HOLSTEIN,
        help_text="Breed of the cow"
    )
    
    # Relationships
    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_cows',
        limit_choices_to={'role': User.Role.FARMER},
        help_text="Farmer who owns this cow"
    )
    
    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name='cows',
        help_text="Farm where the cow is located"
    )
    
    # Physical characteristics
    date_of_birth = models.DateField(
        help_text="Cow's date of birth"
    )
    
    weight_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Current weight in kilograms"
    )
    
    height_cm = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Height in centimeters"
    )
    
    # Status and health
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        help_text="Current status of the cow"
    )
    
    is_pregnant = models.BooleanField(
        default=False,
        help_text="Whether the cow is currently pregnant"
    )
    
    last_breeding_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date of last breeding"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cows'
        verbose_name = 'Cow'
        verbose_name_plural = 'Cows'
        ordering = ['tag_number']
    
    def __str__(self):
        return f"{self.tag_number} - {self.name or 'Unnamed'} ({self.get_breed_display()})"
    
    @property
    def age_years(self):
        """Calculate cow's age in years"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
