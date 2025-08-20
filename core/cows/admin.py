from django.contrib import admin
from .models import Cow

@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    """Admin for Cow model"""
    
    list_display = ('tag_number', 'name', 'breed', 'farmer', 'farm', 'status', 'age_years', 'is_pregnant', 'created_at')
    list_filter = ('breed', 'status', 'is_pregnant', 'created_at', 'farmer__role', 'farm')
    search_fields = ('tag_number', 'name', 'farmer__username', 'farmer__first_name', 'farmer__last_name', 'farm__name')
    ordering = ('tag_number',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tag_number', 'name', 'breed', 'farmer', 'farm')
        }),
        ('Physical Characteristics', {
            'fields': ('date_of_birth', 'weight_kg', 'height_cm')
        }),
        ('Status & Health', {
            'fields': ('status', 'is_pregnant', 'last_breeding_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'age_years')
    
    def get_queryset(self, request):
        """Filter cows based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == 'FARMER':
            return qs.filter(farmer=request.user)
        elif request.user.role == 'AGENT':
            return qs.filter(farm__agent=request.user)
        return qs.none()
