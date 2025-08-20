"""
FarmHub Reporting Service - FastAPI Application
Read-only reporting service that connects to the Django core database
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
from datetime import date, datetime, timedelta

from database import get_db, SessionLocal
from models import User, Farm, Cow, MilkRecord, Activity
from schemas import (
    UserResponse, FarmResponse, CowResponse, 
    MilkRecordResponse, ActivityResponse,
    ProductionSummary, ActivitySummary
)

# Initialize FastAPI app
app = FastAPI(
    title="FarmHub Reporting Service",
    description="Read-only reporting and analytics service for FarmHub system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["GET"],  # Only allow GET requests for read-only service
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "FarmHub Reporting Service",
        "version": "1.0.0",
        "description": "Read-only reporting and analytics for FarmHub",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "users": "/users",
            "farms": "/farms", 
            "cows": "/cows",
            "milk_records": "/milk-records",
            "activities": "/activities",
            "reports": "/reports"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

# User endpoints
@app.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    role: Optional[str] = Query(None),
    db: SessionLocal = Depends(get_db)
):
    """Get list of users with optional filtering"""
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: SessionLocal = Depends(get_db)):
    """Get specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Farm endpoints
@app.get("/farms", response_model=List[FarmResponse])
async def get_farms(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = Query(None),
    db: SessionLocal = Depends(get_db)
):
    """Get list of farms with optional filtering"""
    query = db.query(Farm)
    
    if is_active is not None:
        query = query.filter(Farm.is_active == is_active)
    
    farms = query.offset(skip).limit(limit).all()
    return farms

@app.get("/farms/{farm_id}", response_model=FarmResponse)
async def get_farm(farm_id: int, db: SessionLocal = Depends(get_db)):
    """Get specific farm by ID"""
    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm

# Cow endpoints
@app.get("/cows", response_model=List[CowResponse])
async def get_cows(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    breed: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    farm_id: Optional[int] = Query(None),
    db: SessionLocal = Depends(get_db)
):
    """Get list of cows with optional filtering"""
    query = db.query(Cow)
    
    if breed:
        query = query.filter(Cow.breed == breed)
    if status:
        query = query.filter(Cow.status == status)
    if farm_id:
        query = query.filter(Cow.farm_id == farm_id)
    
    cows = query.offset(skip).limit(limit).all()
    return cows

@app.get("/cows/{cow_id}", response_model=CowResponse)
async def get_cow(cow_id: int, db: SessionLocal = Depends(get_db)):
    """Get specific cow by ID"""
    cow = db.query(Cow).filter(Cow.id == cow_id).first()
    if not cow:
        raise HTTPException(status_code=404, detail="Cow not found")
    return cow

# Milk record endpoints
@app.get("/milk-records", response_model=List[MilkRecordResponse])
async def get_milk_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    cow_id: Optional[int] = Query(None),
    farm_id: Optional[int] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    db: SessionLocal = Depends(get_db)
):
    """Get milk records with optional filtering"""
    query = db.query(MilkRecord)
    
    if cow_id:
        query = query.filter(MilkRecord.cow_id == cow_id)
    if farm_id:
        query = query.filter(MilkRecord.farm_id == farm_id)
    if from_date:
        query = query.filter(MilkRecord.date >= from_date)
    if to_date:
        query = query.filter(MilkRecord.date <= to_date)
    
    records = query.order_by(MilkRecord.date.desc()).offset(skip).limit(limit).all()
    return records

# Activity endpoints
@app.get("/activities", response_model=List[ActivityResponse])
async def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    cow_id: Optional[int] = Query(None),
    activity_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    db: SessionLocal = Depends(get_db)
):
    """Get activities with optional filtering"""
    query = db.query(Activity)
    
    if cow_id:
        query = query.filter(Activity.cow_id == cow_id)
    if activity_type:
        query = query.filter(Activity.activity_type == activity_type)
    if status:
        query = query.filter(Activity.status == status)
    if from_date:
        query = query.filter(Activity.scheduled_date >= from_date)
    if to_date:
        query = query.filter(Activity.scheduled_date <= to_date)
    
    activities = query.order_by(Activity.scheduled_date.desc()).offset(skip).limit(limit).all()
    return activities

# Reporting endpoints
@app.get("/reports/production-summary", response_model=ProductionSummary)
async def get_production_summary(
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    farm_id: Optional[int] = Query(None),
    db: SessionLocal = Depends(get_db)
):
    """Get milk production summary report"""
    query = db.query(MilkRecord)
    
    if from_date:
        query = query.filter(MilkRecord.date >= from_date)
    if to_date:
        query = query.filter(MilkRecord.date <= to_date)
    if farm_id:
        query = query.filter(MilkRecord.farm_id == farm_id)
    
    records = query.all()
    
    if not records:
        return ProductionSummary(
            total_records=0,
            total_quantity_liters=0.0,
            average_quantity_liters=0.0,
            total_farms=0,
            total_cows=0,
            date_range={"from_date": from_date, "to_date": to_date}
        )
    
    total_quantity = sum(record.total_quantity_liters for record in records)
    average_quantity = total_quantity / len(records) if records else 0
    total_farms = len(set(record.farm_id for record in records))
    total_cows = len(set(record.cow_id for record in records))
    
    return ProductionSummary(
        total_records=len(records),
        total_quantity_liters=float(total_quantity),
        average_quantity_liters=float(average_quantity),
        total_farms=total_farms,
        total_cows=total_cows,
        date_range={"from_date": from_date, "to_date": to_date}
    )

@app.get("/reports/activity-summary", response_model=ActivitySummary)
async def get_activity_summary(
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    farm_id: Optional[int] = Query(None),
    db: SessionLocal = Depends(get_db)
):
    """Get activity summary report"""
    query = db.query(Activity)
    
    if from_date:
        query = query.filter(Activity.scheduled_date >= from_date)
    if to_date:
        query = query.filter(Activity.scheduled_date <= to_date)
    if farm_id:
        query = query.join(Cow).filter(Cow.farm_id == farm_id)
    
    activities = query.all()
    
    if not activities:
        return ActivitySummary(
            total_activities=0,
            completed_activities=0,
            planned_activities=0,
            total_cost=0.0,
            activity_types={},
            date_range={"from_date": from_date, "to_date": to_date}
        )
    
    completed = len([a for a in activities if a.status == 'COMPLETED'])
    planned = len([a for a in activities if a.status == 'PLANNED'])
    total_cost = sum(a.cost or 0 for a in activities)
    
    # Activity type distribution
    activity_types = {}
    for activity in activities:
        activity_types[activity.activity_type] = activity_types.get(activity.activity_type, 0) + 1
    
    return ActivitySummary(
        total_activities=len(activities),
        completed_activities=completed,
        planned_activities=planned,
        total_cost=float(total_cost),
        activity_types=activity_types,
        date_range={"from_date": from_date, "to_date": to_date}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
