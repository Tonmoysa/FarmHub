from django.db import models
from users.models import User

class Farm(models.Model):
    """
    Farm model representing a farm in the system
    """
    name = models.CharField(
        max_length=255,
        help_text="Name of the farm"
    )
    
    agent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managed_farms',
        limit_choices_to={'role': User.Role.AGENT},
        help_text="Agent responsible for this farm"
    )
    
    location = models.CharField(
        max_length=500,
        help_text="Farm location/address"
    )
    
    size_acres = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Farm size in acres"
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the farm"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the farm is currently active"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'farms'
        verbose_name = 'Farm'
        verbose_name_plural = 'Farms'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} (Managed by {self.agent.username})"
