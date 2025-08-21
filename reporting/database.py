"""
Database configuration for FastAPI reporting service
Connects to the Django database in read-only mode
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL - use environment variable for production, fallback to local SQLite
DATABASE_URL = os.environ.get('DATABASE_URL', "sqlite:///../core/db.sqlite3")

# Handle PostgreSQL URL format for Render
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine with appropriate configuration
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration for local development
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,  # Required for SQLite with FastAPI
            "uri": True
        },
        echo=False,  # Set to True for SQL debugging
        pool_pre_ping=True
    )
else:
    # PostgreSQL configuration for production
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20
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
