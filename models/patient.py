from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class PatientBase(BaseModel):
    """Base model for patient data."""
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: str = Field(..., description="Patient's gender (Male, Female, Other)")
    phone_number: str
    email: Optional[str] = None
    address: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_id: Optional[str] = None


class Patient(PatientBase):
    """Patient model with ID."""
    id: int = Field(..., description="Unique identifier for the patient")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class PatientCreate(PatientBase):
    """Model for creating a new patient."""
    pass


class PatientUpdate(BaseModel):
    """Model for updating patient information."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_id: Optional[str] = None