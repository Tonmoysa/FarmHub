from rest_framework import serializers
from .models import Cow
from users.serializers import UserSerializer
from farms.serializers import FarmSerializer
from users.models import User
from farms.models import Farm

class CowSerializer(serializers.ModelSerializer):
    """Serializer for Cow model"""
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
    age_years = serializers.ReadOnlyField()
    
    class Meta:
        model = Cow
        fields = [
            'id', 'tag_number', 'name', 'breed', 'farmer', 'farmer_id',
            'farm', 'farm_id', 'date_of_birth', 'weight_kg', 'height_cm',
            'status', 'is_pregnant', 'last_breeding_date', 'age_years',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'age_years', 'created_at', 'updated_at']

class CowListSerializer(serializers.ModelSerializer):
    """Simplified serializer for cow lists"""
    farmer_name = serializers.CharField(source='farmer.get_full_name', read_only=True)
    farm_name = serializers.CharField(source='farm.name', read_only=True)
    age_years = serializers.ReadOnlyField()
    milk_records_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Cow
        fields = [
            'id', 'tag_number', 'name', 'breed', 'farmer_name', 'farm_name',
            'status', 'is_pregnant', 'age_years', 'milk_records_count', 'created_at'
        ]
        read_only_fields = ['id', 'age_years', 'created_at']
    
    def get_milk_records_count(self, obj):
        return obj.milk_records.count()
