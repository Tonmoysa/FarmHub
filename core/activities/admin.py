from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin for Activity model"""
    
    list_display = ('title', 'cow', 'activity_type', 'status', 'scheduled_date', 'scheduled_time', 'created_at')
    list_filter = ('activity_type', 'status', 'scheduled_date', 'created_at', 'cow__breed', 'cow__farm')
    search_fields = ('title', 'cow__tag_number', 'cow__name', 'description', 'notes')
    ordering = ('-scheduled_date', '-scheduled_time')
    date_hierarchy = 'scheduled_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'activity_type', 'cow')
        }),
        ('Scheduling', {
            'fields': ('scheduled_date', 'scheduled_time', 'start_time', 'end_time')
        }),
        ('Status & Details', {
            'fields': ('status', 'description', 'notes')
        }),
        ('Cost', {
            'fields': ('cost',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'duration_minutes', 'is_overdue')
    
    def get_queryset(self, request):
        """Filter activities based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == 'FARMER':
            return qs.filter(cow__farmer=request.user)
        elif request.user.role == 'AGENT':
            return qs.filter(cow__farm__agent=request.user)
        return qs.none()
