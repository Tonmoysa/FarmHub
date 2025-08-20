from django.contrib import admin
from .models import MilkRecord

@admin.register(MilkRecord)
class MilkRecordAdmin(admin.ModelAdmin):
    """Admin for MilkRecord model"""
    
    list_display = ('cow', 'farmer', 'farm', 'date', 'total_quantity_liters', 'quality_rating', 'created_at')
    list_filter = ('date', 'quality_rating', 'created_at', 'cow__breed', 'farm')
    search_fields = ('cow__tag_number', 'cow__name', 'farmer__username', 'farmer__first_name', 'farmer__last_name', 'farm__name')
    ordering = ('-date', '-created_at')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Relationships', {
            'fields': ('cow', 'farmer', 'farm')
        }),
        ('Production Data', {
            'fields': ('date', 'morning_quantity_liters', 'evening_quantity_liters', 'total_quantity_liters')
        }),
        ('Quality Metrics', {
            'fields': ('fat_percentage', 'protein_percentage', 'quality_rating')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'total_quantity_liters')
    
    def get_queryset(self, request):
        """Filter milk records based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == 'FARMER':
            return qs.filter(farmer=request.user)
        elif request.user.role == 'AGENT':
            return qs.filter(farm__agent=request.user)
        return qs.none()
