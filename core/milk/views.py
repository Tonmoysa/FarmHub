from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import MilkRecord
from .serializers import (
    MilkRecordSerializer, MilkRecordListSerializer, 
    DailyMilkProductionSerializer, BulkMilkProductionSerializer
)
from core_service.permissions import MilkRecordPermission
from django.db import models

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
        elif self.action == 'record_daily_production':
            return DailyMilkProductionSerializer
        elif self.action == 'bulk_record_production':
            return BulkMilkProductionSerializer
        return MilkRecordSerializer
    
    def perform_create(self, serializer):
        """Set farmer automatically for farmers"""
        if self.request.user.is_farmer:
            serializer.save(farmer=self.request.user)
        else:
            serializer.save()
    
    @action(detail=False, methods=['post'], url_path='record-daily')
    def record_daily_production(self, request):
        """Record daily milk production for a single cow"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            milk_record = serializer.save()
            return Response({
                'message': 'Daily milk production recorded successfully',
                'record_id': milk_record.id,
                'cow_tag': milk_record.cow.tag_number,
                'total_quantity': float(milk_record.total_quantity_liters),
                'date': milk_record.date
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='bulk-record')
    def bulk_record_production(self, request):
        """Record daily milk production for multiple cows"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({
                'message': f'Bulk milk production recorded successfully',
                'records_created': result['created_records'],
                'date': result['date']
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='production-summary')
    def production_summary(self, request):
        """Get milk production summary for the user's cows"""
        queryset = self.get_queryset()
        
        # Get date range from query params
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        
        if from_date:
            queryset = queryset.filter(date__gte=from_date)
        if to_date:
            queryset = queryset.filter(date__lte=to_date)
        
        # Calculate summary statistics
        total_records = queryset.count()
        total_quantity = queryset.aggregate(
            total=models.Sum('total_quantity_liters')
        )['total'] or 0
        
        avg_quantity = queryset.aggregate(
            avg=models.Avg('total_quantity_liters')
        )['avg'] or 0
        
        # Get top producing cows
        top_cows = queryset.values('cow__tag_number', 'cow__name').annotate(
            total_production=models.Sum('total_quantity_liters')
        ).order_by('-total_production')[:5]
        
        # Get quality distribution
        quality_distribution = queryset.values('quality_rating').annotate(
            count=models.Count('id')
        ).order_by('quality_rating')
        
        return Response({
            'summary': {
                'total_records': total_records,
                'total_quantity_liters': float(total_quantity),
                'average_quantity_liters': float(avg_quantity),
                'date_range': {
                    'from_date': from_date,
                    'to_date': to_date
                }
            },
            'top_producing_cows': list(top_cows),
            'quality_distribution': list(quality_distribution)
        })
    
    @action(detail=False, methods=['get'], url_path='cow-production/(?P<cow_tag>[^/.]+)')
    def cow_production(self, request, cow_tag=None):
        """Get milk production history for a specific cow"""
        queryset = self.get_queryset().filter(cow__tag_number=cow_tag)
        
        if not queryset.exists():
            return Response({
                'error': f'No milk records found for cow {cow_tag}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get date range from query params
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        
        if from_date:
            queryset = queryset.filter(date__gte=from_date)
        if to_date:
            queryset = queryset.filter(date__lte=to_date)
        
        # Calculate cow-specific statistics
        total_production = queryset.aggregate(
            total=models.Sum('total_quantity_liters')
        )['total'] or 0
        
        avg_production = queryset.aggregate(
            avg=models.Avg('total_quantity_liters')
        )['avg'] or 0
        
        max_production = queryset.aggregate(
            max=models.Max('total_quantity_liters')
        )['max'] or 0
        
        # Get recent records
        recent_records = queryset.order_by('-date')[:10]
        
        return Response({
            'cow_tag': cow_tag,
            'cow_name': queryset.first().cow.name,
            'statistics': {
                'total_production_liters': float(total_production),
                'average_production_liters': float(avg_production),
                'max_production_liters': float(max_production),
                'total_records': queryset.count()
            },
            'recent_records': MilkRecordListSerializer(recent_records, many=True).data
        })
