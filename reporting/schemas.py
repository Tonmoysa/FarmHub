"""
Pydantic models for API request/response schemas
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import date, datetime, time
from decimal import Decimal

class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    model_config = ConfigDict(from_attributes=True)

# User schemas
class UserResponse(BaseSchema):
    id: int
    username: str
    email: Optional[str] = None
    first_name: str
    last_name: str
    role: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    is_active: bool
    created_at: Optional[datetime] = None

# Farm schemas
class FarmResponse(BaseSchema):
    id: int
    name: str
    agent_id: int
    location: str
    size_acres: Optional[Decimal] = None
    description: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None

# Cow schemas
class CowResponse(BaseSchema):
    id: int
    tag_number: str
    name: Optional[str] = None
    breed: str
    farmer_id: int
    farm_id: int
    date_of_birth: date
    weight_kg: Optional[Decimal] = None
    height_cm: Optional[Decimal] = None
    status: str
    is_pregnant: bool
    last_breeding_date: Optional[date] = None
    created_at: Optional[datetime] = None

# Milk record schemas
class MilkRecordResponse(BaseSchema):
    id: int
    cow_id: int
    farmer_id: int
    farm_id: int
    date: date
    morning_quantity_liters: Decimal
    evening_quantity_liters: Decimal
    total_quantity_liters: Decimal
    fat_percentage: Optional[Decimal] = None
    protein_percentage: Optional[Decimal] = None
    quality_rating: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

# Activity schemas
class ActivityResponse(BaseSchema):
    id: int
    title: str
    activity_type: str
    cow_id: int
    scheduled_date: date
    scheduled_time: Optional[time] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str
    description: Optional[str] = None
    notes: Optional[str] = None
    cost: Optional[Decimal] = None
    created_at: Optional[datetime] = None

# Report schemas
class ProductionSummary(BaseSchema):
    total_records: int
    total_quantity_liters: float
    average_quantity_liters: float
    total_farms: int
    total_cows: int
    date_range: Dict[str, Optional[date]]

class ActivitySummary(BaseSchema):
    total_activities: int
    completed_activities: int
    planned_activities: int
    total_cost: float
    activity_types: Dict[str, int]
    date_range: Dict[str, Optional[date]]

# Enhanced response schemas with relationships
class CowWithRelations(CowResponse):
    farmer: Optional[UserResponse] = None
    farm: Optional[FarmResponse] = None

class MilkRecordWithRelations(MilkRecordResponse):
    cow: Optional[CowResponse] = None
    farmer: Optional[UserResponse] = None
    farm: Optional[FarmResponse] = None

class ActivityWithRelations(ActivityResponse):
    cow: Optional[CowResponse] = None

class FarmWithRelations(FarmResponse):
    agent: Optional[UserResponse] = None
    cow_count: Optional[int] = None
    total_milk_production: Optional[float] = None

# Dashboard and analytics schemas
class DashboardSummary(BaseSchema):
    total_farms: int
    total_cows: int
    total_farmers: int
    active_farms: int
    milk_production_today: float
    activities_completed_today: int
    activities_pending: int

class FarmProductionReport(BaseSchema):
    farm_id: int
    farm_name: str
    agent_name: str
    total_cows: int
    active_cows: int
    total_production_liters: float
    average_production_per_cow: float
    production_trend: List[Dict[str, Any]]

class CowProductionReport(BaseSchema):
    cow_id: int
    cow_tag: str
    cow_name: Optional[str] = None
    breed: str
    farmer_name: str
    farm_name: str
    total_production_liters: float
    average_daily_production: float
    production_trend: List[Dict[str, Any]]
    latest_activity: Optional[ActivityResponse] = None

class HealthReport(BaseSchema):
    total_health_checks: int
    healthy_cows: int
    sick_cows: int
    recovering_cows: int
    pending_vaccinations: int
    recent_calvings: int
    breeding_schedule: List[Dict[str, Any]]

class FinancialReport(BaseSchema):
    total_activity_costs: float
    vaccination_costs: float
    health_check_costs: float
    medication_costs: float
    monthly_breakdown: List[Dict[str, Any]]
    cost_per_farm: List[Dict[str, Any]]
