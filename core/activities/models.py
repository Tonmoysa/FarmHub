from django.db import models
from cows.models import Cow

class Activity(models.Model):
    """
    Activity model for tracking various farm activities related to cows
    """
    class ActivityType(models.TextChoices):
        MILKING = 'MILKING', 'Milking'
        FEEDING = 'FEEDING', 'Feeding'
        HEALTH_CHECK = 'HEALTH_CHECK', 'Health Check'
        VACCINATION = 'VACCINATION', 'Vaccination'
        BREEDING = 'BREEDING', 'Breeding'
        CALVING = 'CALVING', 'Calving'
        WEIGHING = 'WEIGHING', 'Weighing'
        MEDICATION = 'MEDICATION', 'Medication'
        CLEANING = 'CLEANING', 'Cleaning'
        MAINTENANCE = 'MAINTENANCE', 'Maintenance'
        OTHER = 'OTHER', 'Other'
    
    class Status(models.TextChoices):
        PLANNED = 'PLANNED', 'Planned'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    # Basic information
    title = models.CharField(
        max_length=255,
        help_text="Title of the activity"
    )
    
    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
        help_text="Type of activity"
    )
    
    # Relationships
    cow = models.ForeignKey(
        Cow,
        on_delete=models.CASCADE,
        related_name='activities',
        help_text="Cow associated with this activity"
    )
    
    # Timing
    scheduled_date = models.DateField(
        help_text="Scheduled date for the activity"
    )
    
    scheduled_time = models.TimeField(
        blank=True,
        null=True,
        help_text="Scheduled time for the activity"
    )
    
    start_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Actual start time of the activity"
    )
    
    end_time = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Actual end time of the activity"
    )
    
    # Status and details
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED,
        help_text="Current status of the activity"
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of the activity"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about the activity"
    )
    
    # Cost and resources
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Cost associated with this activity"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'activities'
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
        ordering = ['-scheduled_date', '-scheduled_time']
    
    def __str__(self):
        return f"{self.title} - {self.cow.tag_number} ({self.get_activity_type_display()})"
    
    @property
    def duration_minutes(self):
        """Calculate activity duration in minutes"""
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            return duration.total_seconds() / 60
        return None
    
    @property
    def is_overdue(self):
        """Check if the activity is overdue"""
        from datetime import datetime
        if self.status == Activity.Status.PLANNED:
            scheduled_datetime = datetime.combine(self.scheduled_date, self.scheduled_time or datetime.min.time())
            return scheduled_datetime < datetime.now()
        return False
