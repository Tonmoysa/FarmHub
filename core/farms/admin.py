from django.contrib import admin
from .models import Farm

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    """Admin for Farm model"""
    
    list_display = ('name', 'agent', 'location', 'size_acres', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'agent__role')
    search_fields = ('name', 'location', 'agent__username', 'agent__first_name', 'agent__last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'agent', 'location', 'size_acres')
        }),
        ('Details', {
            'fields': ('description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        """Filter farms based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == 'AGENT':
            return qs.filter(agent=request.user)
        return qs.none()
