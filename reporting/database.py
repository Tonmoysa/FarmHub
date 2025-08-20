"""
Database configuration for FastAPI reporting service
Connects to the Django SQLite database in read-only mode
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - point to the Django SQLite database
DATABASE_URL = "sqlite:///../core/db.sqlite3"

# Create engine with read-only configuration
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,  # Required for SQLite with FastAPI
        "uri": True
    },
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base for models
Base = declarative_base()

def get_db():
    """
    Dependency function to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """
    Test database connection
    """
    try:
        db = SessionLocal()
        from sqlalchemy import text
        result = db.execute(text("SELECT 1")).fetchone()
        db.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
