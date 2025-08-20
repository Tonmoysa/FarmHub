from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cow
from .serializers import CowSerializer, CowListSerializer
from core_service.permissions import CowPermission

# Create your views here.

class CowViewSet(viewsets.ModelViewSet):
    """ViewSet for Cow model with role-based access"""
    queryset = Cow.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['breed', 'status', 'is_pregnant', 'farmer__role', 'farm']
    search_fields = ['tag_number', 'name', 'farmer__username', 'farmer__first_name', 'farmer__last_name', 'farm__name']
    ordering_fields = ['tag_number', 'name', 'date_of_birth', 'created_at']
    ordering = ['tag_number']
    permission_classes = [CowPermission]
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        queryset = super().get_queryset()
        
        if self.request.user.is_super_admin:
            return queryset
        
        if self.request.user.is_agent:
            return queryset.filter(farm__agent=self.request.user)
        
        if self.request.user.is_farmer:
            return queryset.filter(farmer=self.request.user)
        
        return queryset.none()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return CowListSerializer
        return CowSerializer
    
    def perform_create(self, serializer):
        """Set farmer automatically for farmers"""
        if self.request.user.is_farmer:
            serializer.save(farmer=self.request.user)
        else:
            serializer.save()
