from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Farm
from .serializers import FarmSerializer, FarmListSerializer
from core_service.permissions import FarmPermission

# Create your views here.

class FarmViewSet(viewsets.ModelViewSet):
    """ViewSet for Farm model with role-based access"""
    queryset = Farm.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'agent__role']
    search_fields = ['name', 'location', 'agent__username', 'agent__first_name', 'agent__last_name']
    ordering_fields = ['name', 'size_acres', 'created_at']
    ordering = ['-created_at']
    permission_classes = [FarmPermission]
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        queryset = super().get_queryset()
        
        if self.request.user.is_super_admin:
            return queryset
        
        if self.request.user.is_agent:
            return queryset.filter(agent=self.request.user)
        
        return queryset.none()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return FarmListSerializer
        return FarmSerializer
    
    def perform_create(self, serializer):
        """Set agent automatically for agents"""
        if self.request.user.is_agent:
            serializer.save(agent=self.request.user)
        else:
            serializer.save()
