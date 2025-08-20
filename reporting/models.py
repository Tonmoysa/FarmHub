"""
SQLAlchemy models that mirror the Django models for read-only access
These models map to the same database tables created by Django
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Time, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    """User model mapping to Django's users table"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True)
    email = Column(String(254))
    first_name = Column(String(150))
    last_name = Column(String(150))
    role = Column(String(20))
    phone_number = Column(String(15))
    address = Column(Text)
    date_of_birth = Column(Date)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime)
    last_login = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Relationships
    managed_farms = relationship("Farm", back_populates="agent")
    owned_cows = relationship("Cow", back_populates="farmer")
    milk_records = relationship("MilkRecord", back_populates="farmer")

class Farm(Base):
    """Farm model mapping to Django's farms table"""
    __tablename__ = "farms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    agent_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String(500))
    size_acres = Column(Numeric(10, 2))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Relationships
    agent = relationship("User", back_populates="managed_farms")
    cows = relationship("Cow", back_populates="farm")
    milk_records = relationship("MilkRecord", back_populates="farm")

class Cow(Base):
    """Cow model mapping to Django's cows table"""
    __tablename__ = "cows"
    
    id = Column(Integer, primary_key=True, index=True)
    tag_number = Column(String(50), unique=True)
    name = Column(String(100))
    breed = Column(String(20))
    farmer_id = Column(Integer, ForeignKey("users.id"))
    farm_id = Column(Integer, ForeignKey("farms.id"))
    date_of_birth = Column(Date)
    weight_kg = Column(Numeric(6, 2))
    height_cm = Column(Numeric(5, 2))
    status = Column(String(20))
    is_pregnant = Column(Boolean, default=False)
    last_breeding_date = Column(Date)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Relationships
    farmer = relationship("User", back_populates="owned_cows")
    farm = relationship("Farm", back_populates="cows")
    milk_records = relationship("MilkRecord", back_populates="cow")
    activities = relationship("Activity", back_populates="cow")

class MilkRecord(Base):
    """MilkRecord model mapping to Django's milk_records table"""
    __tablename__ = "milk_records"
    
    id = Column(Integer, primary_key=True, index=True)
    cow_id = Column(Integer, ForeignKey("cows.id"))
    farmer_id = Column(Integer, ForeignKey("users.id"))
    farm_id = Column(Integer, ForeignKey("farms.id"))
    date = Column(Date)
    morning_quantity_liters = Column(Numeric(6, 2))
    evening_quantity_liters = Column(Numeric(6, 2))
    total_quantity_liters = Column(Numeric(6, 2))
    fat_percentage = Column(Numeric(4, 2))
    protein_percentage = Column(Numeric(4, 2))
    quality_rating = Column(String(20))
    notes = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Relationships
    cow = relationship("Cow", back_populates="milk_records")
    farmer = relationship("User", back_populates="milk_records")
    farm = relationship("Farm", back_populates="milk_records")

class Activity(Base):
    """Activity model mapping to Django's activities table"""
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    activity_type = Column(String(20))
    cow_id = Column(Integer, ForeignKey("cows.id"))
    scheduled_date = Column(Date)
    scheduled_time = Column(Time)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String(20))
    description = Column(Text)
    notes = Column(Text)
    cost = Column(Numeric(10, 2))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Relationships
    cow = relationship("Cow", back_populates="activities")
