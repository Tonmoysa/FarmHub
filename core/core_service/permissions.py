from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """Allow access only to super admins"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_super_admin

class IsAgent(permissions.BasePermission):
    """Allow access only to agents"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_agent

class IsFarmer(permissions.BasePermission):
    """Allow access only to farmers"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_farmer

class IsSuperAdminOrAgent(permissions.BasePermission):
    """Allow access to super admins and agents"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_super_admin or request.user.is_agent)

class IsSuperAdminOrAgentOrFarmer(permissions.BasePermission):
    """Allow access to super admins, agents, and farmers"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_super_admin or 
            request.user.is_agent or 
            request.user.is_farmer
        )

class FarmPermission(permissions.BasePermission):
    """Permission for Farm model - SuperAdmin full access, Agent can manage assigned farms"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_super_admin:
            return True
        
        if request.user.is_agent:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_super_admin:
            return True
        
        if request.user.is_agent:
            return obj.agent == request.user
        
        return False

class CowPermission(permissions.BasePermission):
    """Permission for Cow model - SuperAdmin full access, Agent can see assigned farms' cows, Farmer can manage own cows"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_super_admin:
            return True
        
        if request.user.is_agent or request.user.is_farmer:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_super_admin:
            return True
        
        if request.user.is_agent:
            return obj.farm.agent == request.user
        
        if request.user.is_farmer:
            return obj.farmer == request.user
        
        return False

class MilkRecordPermission(permissions.BasePermission):
    """Permission for MilkRecord model - SuperAdmin full access, Agent can see assigned farms' records, Farmer can manage own records"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_super_admin:
            return True
        
        if request.user.is_agent or request.user.is_farmer:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_super_admin:
            return True
        
        if request.user.is_agent:
            return obj.farm.agent == request.user
        
        if request.user.is_farmer:
            return obj.farmer == request.user
        
        return False

class ActivityPermission(permissions.BasePermission):
    """Permission for Activity model - SuperAdmin full access, Agent can see assigned farms' activities, Farmer can manage own activities"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_super_admin:
            return True
        
        if request.user.is_agent or request.user.is_farmer:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_super_admin:
            return True
        
        if request.user.is_agent:
            return obj.cow.farm.agent == request.user
        
        if request.user.is_farmer:
            return obj.cow.farmer == request.user
        
        return False
