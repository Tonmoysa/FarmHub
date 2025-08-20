from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import MilkRecord
from .serializers import MilkRecordSerializer, MilkRecordListSerializer
from core_service.permissions import MilkRecordPermission

# Create your views here.

class MilkRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for MilkRecord model with role-based access"""
    queryset = MilkRecord.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date', 'quality_rating', 'cow__breed', 'farm']
    search_fields = ['cow__tag_number', 'cow__name', 'farmer__username', 'farmer__first_name', 'farmer__last_name', 'farm__name']
    ordering_fields = ['date', 'total_quantity_liters', 'created_at']
    ordering = ['-date', '-created_at']
    permission_classes = [MilkRecordPermission]
    
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
            return MilkRecordListSerializer
        return MilkRecordSerializer
    
    def perform_create(self, serializer):
        """Set farmer automatically for farmers"""
        if self.request.user.is_farmer:
            serializer.save(farmer=self.request.user)
        else:
            serializer.save()
