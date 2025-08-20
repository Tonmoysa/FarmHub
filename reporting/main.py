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
from sqlalchemy import func, and_

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
            "reports": "/reports",
            "farm_summary": "/reports/farm-summary",
            "milk_production": "/reports/milk-production",
            "recent_activities": "/reports/recent-activities"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db = SessionLocal()
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
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

# NEW ENDPOINTS

@app.get("/reports/farm-summary")
async def get_farm_summary(
    farm_id: Optional[int] = Query(None),
    db: SessionLocal = Depends(get_db)
):
    """Get farm summary showing number of farmers, cows, and total milk production"""
    
    if farm_id:
        # Get specific farm summary
        farm = db.query(Farm).filter(Farm.id == farm_id).first()
        if not farm:
            raise HTTPException(status_code=404, detail="Farm not found")
        
        # Count farmers (users with FARMER role assigned to this farm)
        farmer_count = db.query(User).join(Cow).filter(
            and_(User.role == 'FARMER', Cow.farm_id == farm_id)
        ).distinct().count()
        
        # Count cows
        cow_count = db.query(Cow).filter(Cow.farm_id == farm_id).count()
        
        # Get total milk production
        total_milk = db.query(func.sum(MilkRecord.total_quantity_liters)).filter(
            MilkRecord.farm_id == farm_id
        ).scalar() or 0
        
        # Get recent milk production (last 30 days)
        thirty_days_ago = date.today() - timedelta(days=30)
        recent_milk = db.query(func.sum(MilkRecord.total_quantity_liters)).filter(
            and_(MilkRecord.farm_id == farm_id, MilkRecord.date >= thirty_days_ago)
        ).scalar() or 0
        
        return {
            "farm_id": farm.id,
            "farm_name": farm.name,
            "agent_name": f"{farm.agent.first_name} {farm.agent.last_name}" if farm.agent else "Unknown",
            "farmer_count": farmer_count,
            "cow_count": cow_count,
            "total_milk_production_liters": float(total_milk),
            "recent_milk_production_liters": float(recent_milk),
            "farm_status": "Active" if farm.is_active else "Inactive",
            "location": farm.location,
            "size_acres": float(farm.size_acres) if farm.size_acres else None
        }
    else:
        # Get summary for all farms
        farms = db.query(Farm).all()
        farm_summaries = []
        
        for farm in farms:
            # Count farmers for this farm
            farmer_count = db.query(User).join(Cow).filter(
                and_(User.role == 'FARMER', Cow.farm_id == farm.id)
            ).distinct().count()
            
            # Count cows for this farm
            cow_count = db.query(Cow).filter(Cow.farm_id == farm.id).count()
            
            # Get total milk production for this farm
            total_milk = db.query(func.sum(MilkRecord.total_quantity_liters)).filter(
                MilkRecord.farm_id == farm.id
            ).scalar() or 0
            
            farm_summaries.append({
                "farm_id": farm.id,
                "farm_name": farm.name,
                "agent_name": f"{farm.agent.first_name} {farm.agent.last_name}" if farm.agent else "Unknown",
                "farmer_count": farmer_count,
                "cow_count": cow_count,
                "total_milk_production_liters": float(total_milk),
                "farm_status": "Active" if farm.is_active else "Inactive"
            })
        
        # Calculate overall totals
        total_farmers = sum(fs["farmer_count"] for fs in farm_summaries)
        total_cows = sum(fs["cow_count"] for fs in farm_summaries)
        total_milk = sum(fs["total_milk_production_liters"] for fs in farm_summaries)
        
        return {
            "overall_summary": {
                "total_farms": len(farms),
                "active_farms": len([f for f in farms if f.is_active]),
                "total_farmers": total_farmers,
                "total_cows": total_cows,
                "total_milk_production_liters": total_milk
            },
            "farm_details": farm_summaries
        }

@app.get("/reports/milk-production")
async def get_milk_production_filtered(
    farm_id: Optional[int] = Query(None),
    farmer_id: Optional[int] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: SessionLocal = Depends(get_db)
):
    """Get milk production filtered by farm, farmer, or date range"""
    
    query = db.query(MilkRecord)
    
    # Apply filters
    if farm_id:
        query = query.filter(MilkRecord.farm_id == farm_id)
    if farmer_id:
        query = query.filter(MilkRecord.farmer_id == farmer_id)
    if from_date:
        query = query.filter(MilkRecord.date >= from_date)
    if to_date:
        query = query.filter(MilkRecord.date <= to_date)
    
    # Get records with related data
    records = query.join(Cow).join(Farm).join(User, MilkRecord.farmer_id == User.id).add_columns(
        Cow.tag_number,
        Cow.name.label('cow_name'),
        Farm.name.label('farm_name'),
        User.first_name.label('farmer_first_name'),
        User.last_name.label('farmer_last_name')
    ).order_by(MilkRecord.date.desc()).limit(limit).all()
    
    # Format response
    production_data = []
    for record, cow_tag, cow_name, farm_name, farmer_first, farmer_last in records:
        production_data.append({
            "record_id": record.id,
            "date": record.date,
            "cow_tag": cow_tag,
            "cow_name": cow_name,
            "farm_name": farm_name,
            "farmer_name": f"{farmer_first} {farmer_last}",
            "morning_quantity_liters": float(record.morning_quantity_liters),
            "evening_quantity_liters": float(record.evening_quantity_liters),
            "total_quantity_liters": float(record.total_quantity_liters),
            "fat_percentage": float(record.fat_percentage) if record.fat_percentage else None,
            "protein_percentage": float(record.protein_percentage) if record.protein_percentage else None,
            "quality_rating": record.quality_rating
        })
    
    # Calculate summary statistics
    total_records = len(production_data)
    total_quantity = sum(r["total_quantity_liters"] for r in production_data)
    average_quantity = total_quantity / total_records if total_records > 0 else 0
    
    return {
        "filters_applied": {
            "farm_id": farm_id,
            "farmer_id": farmer_id,
            "from_date": from_date,
            "to_date": to_date
        },
        "summary": {
            "total_records": total_records,
            "total_quantity_liters": total_quantity,
            "average_quantity_liters": average_quantity
        },
        "production_records": production_data
    }

@app.get("/reports/recent-activities")
async def get_recent_activities_summary(
    days: int = Query(7, ge=1, le=90, description="Number of days to look back"),
    activity_type: Optional[str] = Query(None),
    farm_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: SessionLocal = Depends(get_db)
):
    """Get recent activity summaries for the specified number of days"""
    
    # Calculate date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    query = db.query(Activity)
    
    # Apply filters
    query = query.filter(Activity.scheduled_date >= start_date)
    query = query.filter(Activity.scheduled_date <= end_date)
    
    if activity_type:
        query = query.filter(Activity.activity_type == activity_type)
    if farm_id:
        query = query.join(Cow).filter(Cow.farm_id == farm_id)
    
    # Get activities with related data
    activities = query.join(Cow).join(Farm).add_columns(
        Cow.tag_number,
        Cow.name.label('cow_name'),
        Farm.name.label('farm_name')
    ).order_by(Activity.scheduled_date.desc(), Activity.scheduled_time.desc()).limit(limit).all()
    
    # Format response
    activity_data = []
    for activity, cow_tag, cow_name, farm_name in activities:
        activity_data.append({
            "activity_id": activity.id,
            "title": activity.title,
            "activity_type": activity.activity_type,
            "scheduled_date": activity.scheduled_date,
            "scheduled_time": activity.scheduled_time,
            "status": activity.status,
            "cow_tag": cow_tag,
            "cow_name": cow_name,
            "farm_name": farm_name,
            "description": activity.description,
            "cost": float(activity.cost) if activity.cost else None,
            "notes": activity.notes
        })
    
    # Calculate summary statistics
    total_activities = len(activity_data)
    completed_activities = len([a for a in activity_data if a["status"] == "COMPLETED"])
    planned_activities = len([a for a in activity_data if a["status"] == "PLANNED"])
    total_cost = sum(a["cost"] or 0 for a in activity_data)
    
    # Activity type distribution
    activity_types = {}
    for activity in activity_data:
        activity_types[activity["activity_type"]] = activity_types.get(activity["activity_type"], 0) + 1
    
    # Daily activity breakdown
    daily_breakdown = {}
    for activity in activity_data:
        date_str = str(activity["scheduled_date"])
        if date_str not in daily_breakdown:
            daily_breakdown[date_str] = {"total": 0, "completed": 0, "planned": 0}
        daily_breakdown[date_str]["total"] += 1
        if activity["status"] == "COMPLETED":
            daily_breakdown[date_str]["completed"] += 1
        elif activity["status"] == "PLANNED":
            daily_breakdown[date_str]["planned"] += 1
    
    return {
        "date_range": {
            "start_date": start_date,
            "end_date": end_date,
            "days_covered": days
        },
        "filters_applied": {
            "activity_type": activity_type,
            "farm_id": farm_id
        },
        "summary": {
            "total_activities": total_activities,
            "completed_activities": completed_activities,
            "planned_activities": planned_activities,
            "total_cost": total_cost,
            "completion_rate": (completed_activities / total_activities * 100) if total_activities > 0 else 0
        },
        "activity_type_distribution": activity_types,
        "daily_breakdown": daily_breakdown,
        "recent_activities": activity_data
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
