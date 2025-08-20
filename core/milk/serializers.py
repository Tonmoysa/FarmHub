from rest_framework import serializers
from .models import MilkRecord
from users.serializers import UserSerializer
from farms.serializers import FarmSerializer
from cows.serializers import CowSerializer
from cows.models import Cow
from users.models import User
from farms.models import Farm
from datetime import date

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

class DailyMilkProductionSerializer(serializers.ModelSerializer):
    """Serializer for recording daily milk production"""
    cow_tag = serializers.CharField(write_only=True, help_text="Cow tag number")
    farm_name = serializers.CharField(write_only=True, help_text="Farm name")
    
    class Meta:
        model = MilkRecord
        fields = [
            'cow_tag', 'farm_name', 'date', 'morning_quantity_liters', 
            'evening_quantity_liters', 'fat_percentage', 'protein_percentage',
            'quality_rating', 'notes'
        ]
    
    def validate(self, data):
        """Validate the milk production data"""
        cow_tag = data.get('cow_tag')
        farm_name = data.get('farm_name')
        production_date = data.get('date')
        user = self.context['request'].user
        
        # Validate cow exists and belongs to the farmer
        try:
            if user.is_farmer:
                cow = Cow.objects.get(tag_number=cow_tag, farmer=user)
            elif user.is_agent:
                cow = Cow.objects.get(tag_number=cow_tag, farm__agent=user)
            else:
                cow = Cow.objects.get(tag_number=cow_tag)
        except Cow.DoesNotExist:
            raise serializers.ValidationError(f"Cow with tag {cow_tag} not found or not accessible")
        
        # Validate farm exists and matches cow's farm
        try:
            farm = Farm.objects.get(name=farm_name)
            if cow.farm != farm:
                raise serializers.ValidationError(f"Cow {cow_tag} is not assigned to farm {farm_name}")
        except Farm.DoesNotExist:
            raise serializers.ValidationError(f"Farm {farm_name} not found")
        
        # Check if record already exists for this cow and date
        if MilkRecord.objects.filter(cow=cow, date=production_date).exists():
            raise serializers.ValidationError(f"Milk record already exists for cow {cow_tag} on {production_date}")
        
        # Validate quantities
        morning_qty = data.get('morning_quantity_liters', 0)
        evening_qty = data.get('evening_quantity_liters', 0)
        
        if morning_qty < 0 or evening_qty < 0:
            raise serializers.ValidationError("Milk quantities cannot be negative")
        
        if morning_qty > 50 or evening_qty > 50:
            raise serializers.ValidationError("Milk quantities seem unusually high (>50L)")
        
        # Validate quality metrics
        fat_percentage = data.get('fat_percentage')
        protein_percentage = data.get('protein_percentage')
        
        if fat_percentage is not None and (fat_percentage < 0 or fat_percentage > 10):
            raise serializers.ValidationError("Fat percentage must be between 0 and 10")
        
        if protein_percentage is not None and (protein_percentage < 0 or protein_percentage > 10):
            raise serializers.ValidationError("Protein percentage must be between 0 and 10")
        
        # Add validated data
        data['cow'] = cow
        data['farm'] = farm
        data['farmer'] = cow.farmer
        
        return data
    
    def create(self, validated_data):
        """Create milk record with automatic total calculation"""
        cow_tag = validated_data.pop('cow_tag')
        farm_name = validated_data.pop('farm_name')
        
        # Calculate total quantity
        morning_qty = validated_data.get('morning_quantity_liters', 0)
        evening_qty = validated_data.get('evening_quantity_liters', 0)
        validated_data['total_quantity_liters'] = morning_qty + evening_qty
        
        return super().create(validated_data)

class BulkMilkProductionSerializer(serializers.Serializer):
    """Serializer for bulk milk production recording"""
    date = serializers.DateField(help_text="Production date")
    records = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of milk production records"
    )
    
    def validate(self, data):
        """Validate bulk milk production data"""
        production_date = data.get('date')
        records = data.get('records', [])
        user = self.context['request'].user
        
        if not records:
            raise serializers.ValidationError("At least one milk record is required")
        
        if len(records) > 50:
            raise serializers.ValidationError("Cannot process more than 50 records at once")
        
        # Validate each record
        validated_records = []
        for i, record in enumerate(records):
            try:
                # Create a temporary serializer for validation
                temp_data = {**record, 'date': production_date}
                serializer = DailyMilkProductionSerializer(data=temp_data, context=self.context)
                if serializer.is_valid():
                    validated_records.append(serializer.validated_data)
                else:
                    raise serializers.ValidationError(f"Record {i+1}: {serializer.errors}")
            except Exception as e:
                raise serializers.ValidationError(f"Record {i+1}: {str(e)}")
        
        data['validated_records'] = validated_records
        return data
    
    def create(self, validated_data):
        """Create multiple milk records"""
        records = validated_data['validated_records']
        created_records = []
        
        for record_data in records:
            record = MilkRecord.objects.create(**record_data)
            created_records.append(record)
        
        return {'created_records': len(created_records), 'date': validated_data['date']}
