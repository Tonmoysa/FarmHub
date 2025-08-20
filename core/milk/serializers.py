from rest_framework import serializers
from .models import MilkRecord
from users.serializers import UserSerializer
from farms.serializers import FarmSerializer
from cows.serializers import CowSerializer
from cows.models import Cow
from users.models import User
from farms.models import Farm

class MilkRecordSerializer(serializers.ModelSerializer):
    """Serializer for MilkRecord model"""
    cow = CowSerializer(read_only=True)
    cow_id = serializers.PrimaryKeyRelatedField(
        queryset=Cow.objects.all(),
        source='cow',
        write_only=True
    )
    farmer = UserSerializer(read_only=True)
    farmer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='FARMER'),
        source='farmer',
        write_only=True
    )
    farm = FarmSerializer(read_only=True)
    farm_id = serializers.PrimaryKeyRelatedField(
        queryset=Farm.objects.all(),
        source='farm',
        write_only=True
    )
    
    class Meta:
        model = MilkRecord
        fields = [
            'id', 'cow', 'cow_id', 'farmer', 'farmer_id', 'farm', 'farm_id',
            'date', 'morning_quantity_liters', 'evening_quantity_liters',
            'total_quantity_liters', 'fat_percentage', 'protein_percentage',
            'quality_rating', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_quantity_liters', 'created_at', 'updated_at']

class MilkRecordListSerializer(serializers.ModelSerializer):
    """Simplified serializer for milk record lists"""
    cow_name = serializers.CharField(source='cow.name', read_only=True)
    cow_tag = serializers.CharField(source='cow.tag_number', read_only=True)
    farmer_name = serializers.CharField(source='farmer.get_full_name', read_only=True)
    farm_name = serializers.CharField(source='farm.name', read_only=True)
    
    class Meta:
        model = MilkRecord
        fields = [
            'id', 'cow_name', 'cow_tag', 'farmer_name', 'farm_name',
            'date', 'total_quantity_liters', 'quality_rating', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
