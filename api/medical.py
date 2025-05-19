from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import (
    Diagnosis as DiagnosisModel, 
    CPTCode as CPTCodeModel,
    PatientDiagnosis as PatientDiagnosisModel,
    PatientProcedure as PatientProcedureModel
)
from models.medical import (
    Diagnosis, DiagnosisCreate,
    CPTCode, CPTCodeCreate,
    PatientDiagnosis, PatientDiagnosisCreate,
    PatientProcedure, PatientProcedureCreate
)

router = APIRouter(
    prefix="/medical",
    tags=["medical"],
    responses={404: {"description": "Not found"}},
)


# Diagnoses endpoints
@router.post("/diagnoses/", response_model=Diagnosis)
def create_diagnosis(diagnosis: DiagnosisCreate, db: Session = Depends(get_db)):
    """
    Create a new diagnosis.
    """
    db_diagnosis = DiagnosisModel(
        icd_code=diagnosis.icd_code,
        description=diagnosis.description,
        severity=diagnosis.severity
    )
    db.add(db_diagnosis)
    db.commit()
    db.refresh(db_diagnosis)
    return db_diagnosis


@router.get("/diagnoses/", response_model=List[Diagnosis])
def read_diagnoses(
    skip: int = 0, 
    limit: int = 100, 
    icd_code: Optional[str] = Query(None, description="Filter by ICD-10 code"),
    severity: Optional[int] = Query(None, description="Filter by severity level"),
    db: Session = Depends(get_db)
):
    """
    Retrieve diagnoses with optional filtering.
    """
    query = db.query(DiagnosisModel)
    
    if icd_code:
        query = query.filter(DiagnosisModel.icd_code.ilike(f"%{icd_code}%"))
    
    if severity is not None:
        query = query.filter(DiagnosisModel.severity == severity)
    
    diagnoses = query.offset(skip).limit(limit).all()
    return diagnoses


@router.get("/diagnoses/{diagnosis_id}", response_model=Diagnosis)
def read_diagnosis(diagnosis_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific diagnosis by ID.
    """
    diagnosis = db.query(DiagnosisModel).filter(DiagnosisModel.id == diagnosis_id).first()
    if diagnosis is None:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return diagnosis


# CPT Codes endpoints
@router.post("/cpt-codes/", response_model=CPTCode)
def create_cpt_code(cpt_code: CPTCodeCreate, db: Session = Depends(get_db)):
    """
    Create a new CPT code.
    """
    db_cpt_code = CPTCodeModel(
        code=cpt_code.code,
        description=cpt_code.description,
        duration_minutes=cpt_code.duration_minutes,
        requires_specialist=cpt_code.requires_specialist
    )
    db.add(db_cpt_code)
    db.commit()
    db.refresh(db_cpt_code)
    return db_cpt_code


@router.get("/cpt-codes/", response_model=List[CPTCode])
def read_cpt_codes(
    skip: int = 0, 
    limit: int = 100, 
    code: Optional[str] = Query(None, description="Filter by CPT code"),
    requires_specialist: Optional[bool] = Query(None, description="Filter by specialist requirement"),
    db: Session = Depends(get_db)
):
    """
    Retrieve CPT codes with optional filtering.
    """
    query = db.query(CPTCodeModel)
    
    if code:
        query = query.filter(CPTCodeModel.code.ilike(f"%{code}%"))
    
    if requires_specialist is not None:
        query = query.filter(CPTCodeModel.requires_specialist == requires_specialist)
    
    cpt_codes = query.offset(skip).limit(limit).all()
    return cpt_codes


@router.get("/cpt-codes/{cpt_code_id}", response_model=CPTCode)
def read_cpt_code(cpt_code_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific CPT code by ID.
    """
    cpt_code = db.query(CPTCodeModel).filter(CPTCodeModel.id == cpt_code_id).first()
    if cpt_code is None:
        raise HTTPException(status_code=404, detail="CPT code not found")
    return cpt_code


# Patient Diagnoses endpoints
@router.post("/patient-diagnoses/", response_model=PatientDiagnosis)
def create_patient_diagnosis(patient_diagnosis: PatientDiagnosisCreate, db: Session = Depends(get_db)):
    """
    Create a new patient diagnosis.
    """
    db_patient_diagnosis = PatientDiagnosisModel(
        patient_id=patient_diagnosis.patient_id,
        diagnosis_id=patient_diagnosis.diagnosis_id,
        diagnosed_date=patient_diagnosis.diagnosed_date,
        notes=patient_diagnosis.notes
    )
    db.add(db_patient_diagnosis)
    db.commit()
    db.refresh(db_patient_diagnosis)
    return db_patient_diagnosis


@router.get("/patient-diagnoses/", response_model=List[PatientDiagnosis])
def read_patient_diagnoses(
    skip: int = 0, 
    limit: int = 100, 
    patient_id: Optional[int] = Query(None, description="Filter by patient ID"),
    diagnosis_id: Optional[int] = Query(None, description="Filter by diagnosis ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve patient diagnoses with optional filtering.
    """
    query = db.query(PatientDiagnosisModel)
    
    if patient_id is not None:
        query = query.filter(PatientDiagnosisModel.patient_id == patient_id)
    
    if diagnosis_id is not None:
        query = query.filter(PatientDiagnosisModel.diagnosis_id == diagnosis_id)
    
    patient_diagnoses = query.offset(skip).limit(limit).all()
    return patient_diagnoses


@router.get("/patient-diagnoses/{patient_diagnosis_id}", response_model=PatientDiagnosis)
def read_patient_diagnosis(patient_diagnosis_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific patient diagnosis by ID.
    """
    patient_diagnosis = db.query(PatientDiagnosisModel).filter(PatientDiagnosisModel.id == patient_diagnosis_id).first()
    if patient_diagnosis is None:
        raise HTTPException(status_code=404, detail="Patient diagnosis not found")
    return patient_diagnosis


# Patient Procedures endpoints
@router.post("/patient-procedures/", response_model=PatientProcedure)
def create_patient_procedure(patient_procedure: PatientProcedureCreate, db: Session = Depends(get_db)):
    """
    Create a new patient procedure.
    """
    db_patient_procedure = PatientProcedureModel(
        patient_id=patient_procedure.patient_id,
        cpt_code_id=patient_procedure.cpt_code_id,
        diagnosis_id=patient_procedure.diagnosis_id,
        ordered_date=patient_procedure.ordered_date,
        priority=patient_procedure.priority,
        notes=patient_procedure.notes
    )
    db.add(db_patient_procedure)
    db.commit()
    db.refresh(db_patient_procedure)
    return db_patient_procedure


@router.get("/patient-procedures/", response_model=List[PatientProcedure])
def read_patient_procedures(
    skip: int = 0, 
    limit: int = 100, 
    patient_id: Optional[int] = Query(None, description="Filter by patient ID"),
    cpt_code_id: Optional[int] = Query(None, description="Filter by CPT code ID"),
    diagnosis_id: Optional[int] = Query(None, description="Filter by diagnosis ID"),
    priority: Optional[int] = Query(None, description="Filter by priority level"),
    db: Session = Depends(get_db)
):
    """
    Retrieve patient procedures with optional filtering.
    """
    query = db.query(PatientProcedureModel)
    
    if patient_id is not None:
        query = query.filter(PatientProcedureModel.patient_id == patient_id)
    
    if cpt_code_id is not None:
        query = query.filter(PatientProcedureModel.cpt_code_id == cpt_code_id)
    
    if diagnosis_id is not None:
        query = query.filter(PatientProcedureModel.diagnosis_id == diagnosis_id)
    
    if priority is not None:
        query = query.filter(PatientProcedureModel.priority == priority)
    
    patient_procedures = query.offset(skip).limit(limit).all()
    return patient_procedures


@router.get("/patient-procedures/{patient_procedure_id}", response_model=PatientProcedure)
def read_patient_procedure(patient_procedure_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific patient procedure by ID.
    """
    patient_procedure = db.query(PatientProcedureModel).filter(PatientProcedureModel.id == patient_procedure_id).first()
    if patient_procedure is None:
        raise HTTPException(status_code=404, detail="Patient procedure not found")
    return patient_procedure