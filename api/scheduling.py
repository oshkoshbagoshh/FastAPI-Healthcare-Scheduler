from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import (
    Appointment as AppointmentModel,
    Patient as PatientModel,
    PatientProcedure as PatientProcedureModel,
    Diagnosis as DiagnosisModel,
    CPTCode as CPTCodeModel,
    TimeSlot as TimeSlotModel,
    Resource as ResourceModel
)
from models.scheduling import (
    Appointment, ScheduleRequest, ScheduleResponse
)
from services.scheduler import SchedulingService

router = APIRouter(
    prefix="/scheduling",
    tags=["scheduling"],
    responses={404: {"description": "Not found"}},
)


@router.post("/optimize/", response_model=ScheduleResponse)
def optimize_schedule(
    request: ScheduleRequest,
    db: Session = Depends(get_db)
):
    """
    Optimize the schedule based on the provided parameters.
    
    This endpoint uses machine learning to create an optimal schedule for patient procedures.
    """
    # Get all required data from the database
    procedures_query = db.query(PatientProcedureModel)
    
    # Apply filters from the request
    if request.patient_ids:
        procedures_query = procedures_query.filter(PatientProcedureModel.patient_id.in_(request.patient_ids))
    
    if request.procedure_ids:
        procedures_query = procedures_query.filter(PatientProcedureModel.id.in_(request.procedure_ids))
    
    procedures = procedures_query.all()
    
    if not procedures:
        return ScheduleResponse(
            appointments=[],
            unscheduled_procedures=[],
            optimization_score=0.0,
            message="No procedures found matching the criteria"
        )
    
    # Get all patients, diagnoses, CPT codes, time slots, and resources
    patients = db.query(PatientModel).all()
    diagnoses = db.query(DiagnosisModel).all()
    cpt_codes = db.query(CPTCodeModel).all()
    
    # Filter time slots by date range and availability
    time_slots = db.query(TimeSlotModel).filter(
        TimeSlotModel.date >= request.start_date,
        TimeSlotModel.date <= request.end_date,
        TimeSlotModel.is_available == True
    ).all()
    
    resources = db.query(ResourceModel).all()
    
    # Create scheduling service
    scheduling_service = SchedulingService()
    
    # Optimize schedule
    schedule_response = scheduling_service.optimize_schedule(
        procedures=procedures,
        patients=patients,
        diagnoses=diagnoses,
        cpt_codes=cpt_codes,
        time_slots=time_slots,
        resources=resources,
        request=request
    )
    
    # Save appointments to database
    for appointment in schedule_response.appointments:
        db_appointment = AppointmentModel(
            patient_id=appointment.patient_id,
            procedure_id=appointment.procedure_id,
            resource_id=appointment.resource_id,
            scheduled_date=appointment.scheduled_date,
            start_time=appointment.start_time,
            end_time=appointment.end_time,
            status=appointment.status,
            notes=appointment.notes
        )
        db.add(db_appointment)
    
    # Update time slots to mark them as unavailable
    for appointment in schedule_response.appointments:
        time_slot = db.query(TimeSlotModel).filter(
            TimeSlotModel.resource_id == appointment.resource_id,
            TimeSlotModel.date == appointment.scheduled_date,
            TimeSlotModel.start_time == appointment.start_time,
            TimeSlotModel.end_time == appointment.end_time
        ).first()
        
        if time_slot:
            time_slot.is_available = False
    
    db.commit()
    
    return schedule_response


@router.get("/appointments/", response_model=List[Appointment])
def read_appointments(
    skip: int = 0, 
    limit: int = 100, 
    patient_id: Optional[int] = Query(None, description="Filter by patient ID"),
    resource_id: Optional[int] = Query(None, description="Filter by resource ID"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """
    Retrieve appointments with optional filtering.
    """
    query = db.query(AppointmentModel)
    
    if patient_id is not None:
        query = query.filter(AppointmentModel.patient_id == patient_id)
    
    if resource_id is not None:
        query = query.filter(AppointmentModel.resource_id == resource_id)
    
    if start_date is not None:
        query = query.filter(AppointmentModel.scheduled_date >= start_date)
    
    if end_date is not None:
        query = query.filter(AppointmentModel.scheduled_date <= end_date)
    
    if status:
        query = query.filter(AppointmentModel.status == status)
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments


@router.get("/appointments/{appointment_id}", response_model=Appointment)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific appointment by ID.
    """
    appointment = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.put("/appointments/{appointment_id}/cancel", response_model=Appointment)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    Cancel an appointment.
    """
    appointment = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Update appointment status
    appointment.status = "cancelled"
    
    # Make the time slot available again
    time_slot = db.query(TimeSlotModel).filter(
        TimeSlotModel.resource_id == appointment.resource_id,
        TimeSlotModel.date == appointment.scheduled_date,
        TimeSlotModel.start_time == appointment.start_time,
        TimeSlotModel.end_time == appointment.end_time
    ).first()
    
    if time_slot:
        time_slot.is_available = True
    
    db.commit()
    db.refresh(appointment)
    return appointment