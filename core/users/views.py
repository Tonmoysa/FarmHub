from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from core_service.permissions import IsSuperAdmin, IsSuperAdminOrAgent

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model with role-based access"""
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    ordering_fields = ['username', 'first_name', 'last_name', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        queryset = super().get_queryset()
        
        if self.request.user.is_super_admin:
            return queryset
        
        if self.request.user.is_agent:
            # Agents can see farmers assigned to their farms
            return queryset.filter(role='FARMER')
        
        # Farmers can only see themselves
        return queryset.filter(id=self.request.user.id)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['create', 'destroy']:
            permission_classes = [IsSuperAdmin]
        else:
            permission_classes = [IsSuperAdminOrAgent]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Set created_by field when creating users"""
        serializer.save()
    
    def perform_update(self, serializer):
        """Custom update logic"""
        serializer.save()
