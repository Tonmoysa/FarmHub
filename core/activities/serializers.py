from rest_framework import serializers
from .models import Activity
from cows.serializers import CowSerializer
from cows.models import Cow
from datetime import datetime, date

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

class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for logging activities with validation"""
    cow_tag = serializers.CharField(write_only=True, help_text="Cow tag number")
    
    class Meta:
        model = Activity
        fields = [
            'cow_tag', 'title', 'activity_type', 'scheduled_date', 'scheduled_time',
            'start_time', 'end_time', 'status', 'description', 'notes', 'cost'
        ]
    
    def validate(self, data):
        """Validate activity data based on type"""
        cow_tag = data.get('cow_tag')
        activity_type = data.get('activity_type')
        scheduled_date = data.get('scheduled_date')
        user = self.context['request'].user
        
        # Validate cow exists and belongs to the user
        try:
            if user.is_farmer:
                cow = Cow.objects.get(tag_number=cow_tag, farmer=user)
            elif user.is_agent:
                cow = Cow.objects.get(tag_number=cow_tag, farm__agent=user)
            else:
                cow = Cow.objects.get(tag_number=cow_tag)
        except Cow.DoesNotExist:
            raise serializers.ValidationError(f"Cow with tag {cow_tag} not found or not accessible")
        
        # Validate activity type specific rules
        if activity_type == 'VACCINATION':
            if not data.get('description'):
                raise serializers.ValidationError("Vaccination description is required")
            if data.get('cost', 0) < 0:
                raise serializers.ValidationError("Vaccination cost cannot be negative")
        
        elif activity_type == 'CALVING':
            if scheduled_date and scheduled_date > date.today():
                raise serializers.ValidationError("Calving date cannot be in the future")
            if not data.get('description'):
                raise serializers.ValidationError("Calving description is required")
        
        elif activity_type == 'HEALTH_CHECK':
            if not data.get('description'):
                raise serializers.ValidationError("Health check description is required")
            if data.get('cost', 0) < 0:
                raise serializers.ValidationError("Health check cost cannot be negative")
        
        elif activity_type == 'BREEDING':
            if scheduled_date and scheduled_date > date.today():
                raise serializers.ValidationError("Breeding date cannot be in the future")
            if not data.get('description'):
                raise serializers.ValidationError("Breeding description is required")
        
        elif activity_type == 'MEDICATION':
            if not data.get('description'):
                raise serializers.ValidationError("Medication description is required")
            if data.get('cost', 0) < 0:
                raise serializers.ValidationError("Medication cost cannot be negative")
        
        # Validate timing
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time")
        
        # Validate scheduled date is not too far in the past for certain activities
        if scheduled_date and activity_type in ['MILKING', 'FEEDING', 'CLEANING']:
            days_diff = (date.today() - scheduled_date).days
            if days_diff > 7:
                raise serializers.ValidationError(f"{activity_type} activities cannot be logged more than 7 days in the past")
        
        # Add validated cow
        data['cow'] = cow
        
        return data
    
    def create(self, validated_data):
        """Create activity with automatic status setting"""
        cow_tag = validated_data.pop('cow_tag')
        
        # Set default status if not provided
        if 'status' not in validated_data:
            validated_data['status'] = 'COMPLETED'
        
        # Set start_time if not provided but end_time is
        if 'end_time' in validated_data and 'start_time' not in validated_data:
            validated_data['start_time'] = datetime.now()
        
        return super().create(validated_data)

class VaccinationLogSerializer(serializers.ModelSerializer):
    """Specialized serializer for vaccination logging"""
    cow_tag = serializers.CharField(write_only=True, help_text="Cow tag number")
    vaccine_name = serializers.CharField(write_only=True, help_text="Name of the vaccine")
    dosage = serializers.CharField(write_only=True, help_text="Dosage information")
    veterinarian = serializers.CharField(write_only=True, help_text="Name of the veterinarian")
    
    class Meta:
        model = Activity
        fields = [
            'cow_tag', 'scheduled_date', 'scheduled_time', 'vaccine_name', 
            'dosage', 'veterinarian', 'cost', 'notes'
        ]
    
    def validate(self, data):
        """Validate vaccination data"""
        cow_tag = data.get('cow_tag')
        user = self.context['request'].user
        
        # Validate cow exists and belongs to the user
        try:
            if user.is_farmer:
                cow = Cow.objects.get(tag_number=cow_tag, farmer=user)
            elif user.is_agent:
                cow = Cow.objects.get(tag_number=cow_tag, farm__agent=user)
            else:
                cow = Cow.objects.get(tag_number=cow_tag)
        except Cow.DoesNotExist:
            raise serializers.ValidationError(f"Cow with tag {cow_tag} not found or not accessible")
        
        # Validate required fields
        if not data.get('vaccine_name'):
            raise serializers.ValidationError("Vaccine name is required")
        
        if not data.get('dosage'):
            raise serializers.ValidationError("Dosage information is required")
        
        if not data.get('veterinarian'):
            raise serializers.ValidationError("Veterinarian name is required")
        
        # Set activity type and title
        data['activity_type'] = 'VACCINATION'
        data['title'] = f"Vaccination: {data['vaccine_name']}"
        data['description'] = f"Vaccine: {data['vaccine_name']}, Dosage: {data['dosage']}, Vet: {data['veterinarian']}"
        data['cow'] = cow
        data['status'] = 'COMPLETED'
        
        return data
    
    def create(self, validated_data):
        """Create activity with vaccination data"""
        # Extract custom fields that don't exist in Activity model
        cow_tag = validated_data.pop('cow_tag', None)
        vaccine_name = validated_data.pop('vaccine_name', None)
        dosage = validated_data.pop('dosage', None)
        veterinarian = validated_data.pop('veterinarian', None)
        
        # Create the activity
        activity = Activity.objects.create(**validated_data)
        
        return activity

class HealthCheckLogSerializer(serializers.ModelSerializer):
    """Specialized serializer for health check logging"""
    cow_tag = serializers.CharField(write_only=True, help_text="Cow tag number")
    health_status = serializers.ChoiceField(
        choices=[('HEALTHY', 'Healthy'), ('SICK', 'Sick'), ('RECOVERING', 'Recovering')],
        write_only=True,
        help_text="Overall health status"
    )
    symptoms = serializers.CharField(required=False, write_only=True, help_text="Any symptoms observed")
    treatment = serializers.CharField(required=False, write_only=True, help_text="Treatment provided")
    veterinarian = serializers.CharField(write_only=True, help_text="Name of the veterinarian")
    
    class Meta:
        model = Activity
        fields = [
            'cow_tag', 'scheduled_date', 'scheduled_time', 'health_status',
            'symptoms', 'treatment', 'veterinarian', 'cost', 'notes'
        ]
    
    def validate(self, data):
        """Validate health check data"""
        cow_tag = data.get('cow_tag')
        health_status = data.get('health_status')
        user = self.context['request'].user
        
        # Validate cow exists and belongs to the user
        try:
            if user.is_farmer:
                cow = Cow.objects.get(tag_number=cow_tag, farmer=user)
            elif user.is_agent:
                cow = Cow.objects.get(tag_number=cow_tag, farm__agent=user)
            else:
                cow = Cow.objects.get(tag_number=cow_tag)
        except Cow.DoesNotExist:
            raise serializers.ValidationError(f"Cow with tag {cow_tag} not found or not accessible")
        
        # Validate required fields
        if not data.get('veterinarian'):
            raise serializers.ValidationError("Veterinarian name is required")
        
        # Set activity type and title
        data['activity_type'] = 'HEALTH_CHECK'
        data['title'] = f"Health Check: {health_status}"
        
        # Build description
        description_parts = [f"Status: {health_status}", f"Vet: {data['veterinarian']}"]
        if data.get('symptoms'):
            description_parts.append(f"Symptoms: {data['symptoms']}")
        if data.get('treatment'):
            description_parts.append(f"Treatment: {data['treatment']}")
        
        data['description'] = " | ".join(description_parts)
        data['cow'] = cow
        data['status'] = 'COMPLETED'
        
        return data
    
    def create(self, validated_data):
        """Create activity with health check data"""
        # Extract custom fields that don't exist in Activity model
        cow_tag = validated_data.pop('cow_tag', None)
        health_status = validated_data.pop('health_status', None)
        symptoms = validated_data.pop('symptoms', None)
        treatment = validated_data.pop('treatment', None)
        veterinarian = validated_data.pop('veterinarian', None)
        
        # Create the activity
        activity = Activity.objects.create(**validated_data)
        
        return activity

class CalvingLogSerializer(serializers.ModelSerializer):
    """Specialized serializer for calving logging"""
    cow_tag = serializers.CharField(write_only=True, help_text="Cow tag number")
    calf_gender = serializers.ChoiceField(
        choices=[('MALE', 'Male'), ('FEMALE', 'Female')],
        write_only=True,
        help_text="Gender of the calf"
    )
    calf_weight = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False, write_only=True,
        help_text="Weight of the calf in kg"
    )
    complications = serializers.CharField(required=False, write_only=True, help_text="Any complications during calving")
    assistance_provided = serializers.BooleanField(default=False, write_only=True, help_text="Whether assistance was provided")
    
    class Meta:
        model = Activity
        fields = [
            'cow_tag', 'scheduled_date', 'scheduled_time', 'calf_gender',
            'calf_weight', 'complications', 'assistance_provided', 'cost', 'notes'
        ]
    
    def validate(self, data):
        """Validate calving data"""
        cow_tag = data.get('cow_tag')
        user = self.context['request'].user
        
        # Validate cow exists and belongs to the user
        try:
            if user.is_farmer:
                cow = Cow.objects.get(tag_number=cow_tag, farmer=user)
            elif user.is_agent:
                cow = Cow.objects.get(tag_number=cow_tag, farm__agent=user)
            else:
                cow = Cow.objects.get(tag_number=cow_tag)
        except Cow.DoesNotExist:
            raise serializers.ValidationError(f"Cow with tag {cow_tag} not found or not accessible")
        
        # Validate calving date
        calving_date = data.get('scheduled_date')
        if calving_date and calving_date > date.today():
            raise serializers.ValidationError("Calving date cannot be in the future")
        
        # Validate calf weight
        calf_weight = data.get('calf_weight')
        if calf_weight is not None and (calf_weight < 0 or calf_weight > 100):
            raise serializers.ValidationError("Calf weight must be between 0 and 100 kg")
        
        # Set activity type and title
        data['activity_type'] = 'CALVING'
        data['title'] = f"Calving: {data['calf_gender']} calf"
        
        # Build description
        description_parts = [f"Calf Gender: {data['calf_gender']}"]
        if calf_weight:
            description_parts.append(f"Weight: {calf_weight} kg")
        if data.get('complications'):
            description_parts.append(f"Complications: {data['complications']}")
        if data.get('assistance_provided'):
            description_parts.append("Assistance provided")
        
        data['description'] = " | ".join(description_parts)
        data['cow'] = cow
        data['status'] = 'COMPLETED'
        
        return data
    
    def create(self, validated_data):
        """Create activity with calving data"""
        # Extract custom fields that don't exist in Activity model
        cow_tag = validated_data.pop('cow_tag', None)
        calf_gender = validated_data.pop('calf_gender', None)
        calf_weight = validated_data.pop('calf_weight', None)
        complications = validated_data.pop('complications', None)
        assistance_provided = validated_data.pop('assistance_provided', None)
        
        # Create the activity
        activity = Activity.objects.create(**validated_data)
        
        return activity
