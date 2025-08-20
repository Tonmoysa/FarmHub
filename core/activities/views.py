from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Activity
from .serializers import ActivitySerializer, ActivityListSerializer
from core_service.permissions import ActivityPermission

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
        return ActivitySerializer
    
    def perform_create(self, serializer):
        """Set farmer automatically for farmers"""
        if self.request.user.is_farmer:
            # Ensure the cow belongs to the farmer
            cow = serializer.validated_data.get('cow')
            if cow and cow.farmer != self.request.user:
                raise PermissionError("You can only create activities for your own cows")
        serializer.save()
