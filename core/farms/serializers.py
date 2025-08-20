from rest_framework import serializers
from .models import Farm
from users.serializers import UserSerializer
from users.models import User

class FarmSerializer(serializers.ModelSerializer):
    """Serializer for Farm model"""
    agent = UserSerializer(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='AGENT'),
        source='agent',
        write_only=True
    )
    
    class Meta:
        model = Farm
        fields = [
            'id', 'name', 'agent', 'agent_id', 'location', 'size_acres',
            'description', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class FarmListSerializer(serializers.ModelSerializer):
    """Simplified serializer for farm lists"""
    agent_name = serializers.CharField(source='agent.get_full_name', read_only=True)
    cow_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Farm
        fields = [
            'id', 'name', 'agent_name', 'location', 'size_acres',
            'is_active', 'cow_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_cow_count(self, obj):
        return obj.cows.count()
