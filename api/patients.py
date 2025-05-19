from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Patient as PatientModel
from models.patient import Patient, PatientCreate, PatientUpdate

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Patient)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """
    Create a new patient.
    """
    db_patient = PatientModel(
        first_name=patient.first_name,
        last_name=patient.last_name,
        date_of_birth=patient.date_of_birth,
        gender=patient.gender,
        phone_number=patient.phone_number,
        email=patient.email,
        address=patient.address,
        insurance_provider=patient.insurance_provider,
        insurance_id=patient.insurance_id
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.get("/", response_model=List[Patient])
def read_patients(
    skip: int = 0, 
    limit: int = 100, 
    name: Optional[str] = Query(None, description="Filter by first or last name"),
    db: Session = Depends(get_db)
):
    """
    Retrieve patients with optional filtering by name.
    """
    query = db.query(PatientModel)
    
    if name:
        query = query.filter(
            (PatientModel.first_name.ilike(f"%{name}%")) | 
            (PatientModel.last_name.ilike(f"%{name}%"))
        )
    
    patients = query.offset(skip).limit(limit).all()
    return patients


@router.get("/{patient_id}", response_model=Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific patient by ID.
    """
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db)):
    """
    Update a patient's information.
    """
    db_patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Update patient fields if provided
    patient_data = patient.dict(exclude_unset=True)
    for key, value in patient_data.items():
        setattr(db_patient, key, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.delete("/{patient_id}", response_model=dict)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Delete a patient.
    """
    db_patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(db_patient)
    db.commit()
    return {"message": f"Patient {patient_id} deleted successfully"}