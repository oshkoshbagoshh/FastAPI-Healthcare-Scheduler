from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment variable or use SQLite as fallback
DATABASE_URL = os.getenv("DATABASE_URL")

# Handle Heroku's postgres:// vs postgresql:// issue
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Use SQLite for local development if no DATABASE_URL is provided
if not DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./healthcare_scheduler.db"
    # SQLite specific arguments
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL for production
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency for getting a database session.

    Yields:
        Session: A SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database by creating all tables."""
    # Import all models to ensure they are registered with the Base
    from database.models import Patient, Diagnosis, CPTCode, PatientDiagnosis, PatientProcedure, Resource, TimeSlot, Appointment

    # Create all tables
    Base.metadata.create_all(bind=engine)
