from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Activity
from .serializers import (
    ActivitySerializer, ActivityListSerializer, ActivityLogSerializer,
    VaccinationLogSerializer, HealthCheckLogSerializer, CalvingLogSerializer
)
from core_service.permissions import ActivityPermission
from django.db import models
from datetime import date, timedelta

# Create your views here.

class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity model with role-based access"""
    queryset = Activity.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activity_type', 'status', 'scheduled_date', 'cow__breed', 'cow__farm']
    search_fields = ['title', 'cow__tag_number', 'cow__name', 'description', 'notes']
    ordering_fields = ['scheduled_date', 'scheduled_time', 'created_at']
    ordering = ['-scheduled_date', '-scheduled_time']
    permission_classes = [ActivityPermission]
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        queryset = super().get_queryset()
        
        if self.request.user.is_super_admin:
            return queryset
        
        if self.request.user.is_agent:
            return queryset.filter(cow__farm__agent=self.request.user)
        
        if self.request.user.is_farmer:
            return queryset.filter(cow__farmer=self.request.user)
        
        return queryset.none()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ActivityListSerializer
        elif self.action == 'log_activity':
            return ActivityLogSerializer
        elif self.action == 'log_vaccination':
            return VaccinationLogSerializer
        elif self.action == 'log_health_check':
            return HealthCheckLogSerializer
        elif self.action == 'log_calving':
            return CalvingLogSerializer
        return ActivitySerializer
    
    def perform_create(self, serializer):
        """Set farmer automatically for farmers"""
        if self.request.user.is_farmer:
            # Ensure the cow belongs to the farmer
            cow = serializer.validated_data.get('cow')
            if cow and cow.farmer != self.request.user:
                raise PermissionError("You can only create activities for your own cows")
        serializer.save()
    
    @action(detail=False, methods=['post'], url_path='log-activity')
    def log_activity(self, request):
        """Log a general activity"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            activity = serializer.save()
            return Response({
                'message': 'Activity logged successfully',
                'activity_id': activity.id,
                'activity_type': activity.activity_type,
                'cow_tag': activity.cow.tag_number,
                'title': activity.title
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='log-vaccination')
    def log_vaccination(self, request):
        """Log a vaccination activity"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            activity = serializer.save()
            return Response({
                'message': 'Vaccination logged successfully',
                'activity_id': activity.id,
                'cow_tag': activity.cow.tag_number,
                'vaccine_name': request.data.get('vaccine_name'),
                'veterinarian': request.data.get('veterinarian')
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='log-health-check')
    def log_health_check(self, request):
        """Log a health check activity"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            activity = serializer.save()
            return Response({
                'message': 'Health check logged successfully',
                'activity_id': activity.id,
                'cow_tag': activity.cow.tag_number,
                'health_status': request.data.get('health_status'),
                'veterinarian': request.data.get('veterinarian')
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='log-calving')
    def log_calving(self, request):
        """Log a calving activity"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            activity = serializer.save()
            return Response({
                'message': 'Calving logged successfully',
                'activity_id': activity.id,
                'cow_tag': activity.cow.tag_number,
                'calf_gender': request.data.get('calf_gender'),
                'calf_weight': request.data.get('calf_weight')
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='activity-summary')
    def activity_summary(self, request):
        """Get activity summary for the user's cows"""
        queryset = self.get_queryset()
        
        # Get date range from query params
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        activity_type = request.query_params.get('activity_type')
        
        if from_date:
            queryset = queryset.filter(scheduled_date__gte=from_date)
        if to_date:
            queryset = queryset.filter(scheduled_date__lte=to_date)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        # Calculate summary statistics
        total_activities = queryset.count()
        completed_activities = queryset.filter(status='COMPLETED').count()
        planned_activities = queryset.filter(status='PLANNED').count()
        
        # Get activity type distribution
        activity_distribution = queryset.values('activity_type').annotate(
            count=models.Count('id')
        ).order_by('-count')
        
        # Get overdue activities
        overdue_activities = queryset.filter(status='PLANNED').extra(
            where=['scheduled_date < CURRENT_DATE']
        ).count()
        
        # Get upcoming activities (next 7 days)
        upcoming_date = date.today() + timedelta(days=7)
        upcoming_activities = queryset.filter(
            status='PLANNED',
            scheduled_date__lte=upcoming_date,
            scheduled_date__gte=date.today()
        ).count()
        
        # Get total cost
        total_cost = queryset.aggregate(
            total=models.Sum('cost')
        )['total'] or 0
        
        return Response({
            'summary': {
                'total_activities': total_activities,
                'completed_activities': completed_activities,
                'planned_activities': planned_activities,
                'overdue_activities': overdue_activities,
                'upcoming_activities': upcoming_activities,
                'total_cost': float(total_cost),
                'date_range': {
                    'from_date': from_date,
                    'to_date': to_date
                }
            },
            'activity_distribution': list(activity_distribution)
        })
    
    @action(detail=False, methods=['get'], url_path='cow-activities/(?P<cow_tag>[^/.]+)')
    def cow_activities(self, request, cow_tag=None):
        """Get activity history for a specific cow"""
        queryset = self.get_queryset().filter(cow__tag_number=cow_tag)
        
        if not queryset.exists():
            return Response({
                'error': f'No activities found for cow {cow_tag}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get date range from query params
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        activity_type = request.query_params.get('activity_type')
        
        if from_date:
            queryset = queryset.filter(scheduled_date__gte=from_date)
        if to_date:
            queryset = queryset.filter(scheduled_date__lte=to_date)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        # Calculate cow-specific statistics
        total_activities = queryset.count()
        completed_activities = queryset.filter(status='COMPLETED').count()
        total_cost = queryset.aggregate(
            total=models.Sum('cost')
        )['total'] or 0
        
        # Get activity type distribution for this cow
        activity_distribution = queryset.values('activity_type').annotate(
            count=models.Count('id')
        ).order_by('-count')
        
        # Get recent activities
        recent_activities = queryset.order_by('-scheduled_date')[:10]
        
        # Get upcoming activities
        upcoming_activities = queryset.filter(
            status='PLANNED',
            scheduled_date__gte=date.today()
        ).order_by('scheduled_date')[:5]
        
        return Response({
            'cow_tag': cow_tag,
            'cow_name': queryset.first().cow.name,
            'statistics': {
                'total_activities': total_activities,
                'completed_activities': completed_activities,
                'total_cost': float(total_cost)
            },
            'activity_distribution': list(activity_distribution),
            'recent_activities': ActivityListSerializer(recent_activities, many=True).data,
            'upcoming_activities': ActivityListSerializer(upcoming_activities, many=True).data
        })
    
    @action(detail=False, methods=['get'], url_path='overdue-activities')
    def overdue_activities(self, request):
        """Get overdue activities"""
        queryset = self.get_queryset().filter(status='PLANNED').extra(
            where=['scheduled_date < CURRENT_DATE']
        ).order_by('scheduled_date')
        
        return Response({
            'overdue_activities': ActivityListSerializer(queryset, many=True).data,
            'count': queryset.count()
        })
    
    @action(detail=False, methods=['get'], url_path='upcoming-activities')
    def upcoming_activities(self, request):
        """Get upcoming activities (next 7 days)"""
        upcoming_date = date.today() + timedelta(days=7)
        
        queryset = self.get_queryset().filter(
            status='PLANNED',
            scheduled_date__lte=upcoming_date,
            scheduled_date__gte=date.today()
        ).order_by('scheduled_date', 'scheduled_time')
        
        return Response({
            'upcoming_activities': ActivityListSerializer(queryset, many=True).data,
            'count': queryset.count(),
            'date_range': {
                'from_date': date.today(),
                'to_date': upcoming_date
            }
        })
