from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel, Field


class Resource(BaseModel):
    """Model for resources like rooms, equipment, etc."""
    id: int = Field(..., description="Unique identifier for the resource")
    name: str = Field(..., description="Name of the resource")
    type: str = Field(..., description="Type of resource (room, equipment, etc.)")
    is_available: bool = Field(default=True, description="Whether the resource is currently available")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ResourceCreate(BaseModel):
    """Model for creating a new resource."""
    name: str
    type: str
    is_available: bool = True


class TimeSlot(BaseModel):
    """Model for available time slots."""
    id: int = Field(..., description="Unique identifier for the time slot")
    resource_id: int = Field(..., description="ID of the associated resource")
    date: datetime = Field(..., description="Date of the time slot")
    start_time: time = Field(..., description="Start time of the slot")
    end_time: time = Field(..., description="End time of the slot")
    is_available: bool = Field(default=True, description="Whether the time slot is available")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TimeSlotCreate(BaseModel):
    """Model for creating a new time slot."""
    resource_id: int
    date: datetime
    start_time: time
    end_time: time
    is_available: bool = True


class Appointment(BaseModel):
    """Model for scheduled appointments."""
    id: int = Field(..., description="Unique identifier for the appointment")
    patient_id: int = Field(..., description="ID of the patient")
    procedure_id: int = Field(..., description="ID of the procedure")
    resource_id: int = Field(..., description="ID of the resource")
    scheduled_date: datetime = Field(..., description="Date of the appointment")
    start_time: time = Field(..., description="Start time of the appointment")
    end_time: time = Field(..., description="End time of the appointment")
    status: str = Field(default="scheduled", description="Status of the appointment (scheduled, completed, cancelled)")
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class AppointmentCreate(BaseModel):
    """Model for creating a new appointment."""
    patient_id: int
    procedure_id: int
    resource_id: int
    scheduled_date: datetime
    start_time: time
    end_time: time
    status: str = "scheduled"
    notes: Optional[str] = None


class ScheduleRequest(BaseModel):
    """Model for requesting a schedule optimization."""
    patient_ids: Optional[List[int]] = None
    procedure_ids: Optional[List[int]] = None
    start_date: datetime
    end_date: datetime
    priority_threshold: Optional[int] = None
    optimize_for: str = Field(default="efficiency", description="Optimization goal (efficiency, patient_preference, urgency)")


class ScheduleResponse(BaseModel):
    """Model for the response to a schedule optimization request."""
    appointments: List[Appointment]
    unscheduled_procedures: List[int] = Field(default_factory=list, description="IDs of procedures that couldn't be scheduled")
    optimization_score: float = Field(..., description="Score indicating how optimal the schedule is")
    message: str