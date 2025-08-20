from rest_framework import serializers
from .models import Activity
from cows.serializers import CowSerializer
from cows.models import Cow

class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    cow = CowSerializer(read_only=True)
    cow_id = serializers.PrimaryKeyRelatedField(
        queryset=Cow.objects.all(),
        source='cow',
        write_only=True
    )
    duration_minutes = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Activity
        fields = [
            'id', 'title', 'activity_type', 'cow', 'cow_id', 'scheduled_date',
            'scheduled_time', 'start_time', 'end_time', 'status', 'description',
            'notes', 'cost', 'duration_minutes', 'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'duration_minutes', 'is_overdue', 'created_at', 'updated_at']

class ActivityListSerializer(serializers.ModelSerializer):
    """Simplified serializer for activity lists"""
    cow_name = serializers.CharField(source='cow.name', read_only=True)
    cow_tag = serializers.CharField(source='cow.tag_number', read_only=True)
    farm_name = serializers.CharField(source='cow.farm.name', read_only=True)
    duration_minutes = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Activity
        fields = [
            'id', 'title', 'activity_type', 'cow_name', 'cow_tag', 'farm_name',
            'scheduled_date', 'scheduled_time', 'status', 'cost', 'duration_minutes',
            'is_overdue', 'created_at'
        ]
        read_only_fields = ['id', 'duration_minutes', 'is_overdue', 'created_at']
