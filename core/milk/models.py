from django.db import models
from users.models import User
from farms.models import Farm
from cows.models import Cow

class MilkRecord(models.Model):
    """
    MilkRecord model for tracking milk production
    """
    class Quality(models.TextChoices):
        EXCELLENT = 'EXCELLENT', 'Excellent'
        GOOD = 'GOOD', 'Good'
        AVERAGE = 'AVERAGE', 'Average'
        POOR = 'POOR', 'Poor'
    
    # Relationships
    cow = models.ForeignKey(
        Cow,
        on_delete=models.CASCADE,
        related_name='milk_records',
        help_text="Cow that produced the milk"
    )
    
    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='milk_records',
        limit_choices_to={'role': User.Role.FARMER},
        help_text="Farmer who recorded the milk production"
    )
    
    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name='milk_records',
        help_text="Farm where the milk was produced"
    )
    
    # Production data
    date = models.DateField(
        help_text="Date of milk production"
    )
    
    morning_quantity_liters = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        help_text="Morning milk quantity in liters"
    )
    
    evening_quantity_liters = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        help_text="Evening milk quantity in liters"
    )
    
    total_quantity_liters = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Total milk quantity for the day in liters"
    )
    
    # Quality metrics
    fat_percentage = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Fat percentage in the milk"
    )
    
    protein_percentage = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Protein percentage in the milk"
    )
    
    quality_rating = models.CharField(
        max_length=20,
        choices=Quality.choices,
        blank=True,
        null=True,
        help_text="Quality rating of the milk"
    )
    
    # Notes and observations
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about the milk production"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'milk_records'
        verbose_name = 'Milk Record'
        verbose_name_plural = 'Milk Records'
        ordering = ['-date', '-created_at']
        unique_together = ['cow', 'date']  # One record per cow per day
    
    def __str__(self):
        return f"{self.cow.tag_number} - {self.date} ({self.total_quantity_liters}L)"
    
    def save(self, *args, **kwargs):
        """Override save to automatically calculate total quantity"""
        if not self.total_quantity_liters:
            self.total_quantity_liters = (self.morning_quantity_liters or 0) + (self.evening_quantity_liters or 0)
        super().save(*args, **kwargs)
