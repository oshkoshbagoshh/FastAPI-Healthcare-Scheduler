from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Diagnosis(BaseModel):
    """Model for medical diagnoses."""
    id: int = Field(..., description="Unique identifier for the diagnosis")
    icd_code: str = Field(..., description="ICD-10 code for the diagnosis")
    description: str = Field(..., description="Description of the diagnosis")
    severity: int = Field(..., ge=1, le=5, description="Severity level from 1 (mild) to 5 (severe)")
    created_at: datetime = Field(default_factory=datetime.now)


class DiagnosisCreate(BaseModel):
    """Model for creating a new diagnosis."""
    icd_code: str
    description: str
    severity: int = Field(..., ge=1, le=5)


class CPTCode(BaseModel):
    """Model for CPT (Current Procedural Terminology) codes."""
    id: int = Field(..., description="Unique identifier for the CPT code")
    code: str = Field(..., description="CPT code")
    description: str = Field(..., description="Description of the procedure")
    duration_minutes: int = Field(..., description="Estimated duration in minutes")
    requires_specialist: bool = Field(default=False, description="Whether the procedure requires a specialist")
    created_at: datetime = Field(default_factory=datetime.now)


class CPTCodeCreate(BaseModel):
    """Model for creating a new CPT code."""
    code: str
    description: str
    duration_minutes: int
    requires_specialist: bool = False


class PatientDiagnosis(BaseModel):
    """Model for linking patients with diagnoses."""
    id: int = Field(..., description="Unique identifier for the patient diagnosis")
    patient_id: int = Field(..., description="ID of the patient")
    diagnosis_id: int = Field(..., description="ID of the diagnosis")
    diagnosed_date: datetime = Field(..., description="Date when the diagnosis was made")
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class PatientDiagnosisCreate(BaseModel):
    """Model for creating a new patient diagnosis."""
    patient_id: int
    diagnosis_id: int
    diagnosed_date: datetime
    notes: Optional[str] = None


class PatientProcedure(BaseModel):
    """Model for linking patients with procedures (CPT codes)."""
    id: int = Field(..., description="Unique identifier for the patient procedure")
    patient_id: int = Field(..., description="ID of the patient")
    cpt_code_id: int = Field(..., description="ID of the CPT code")
    diagnosis_id: Optional[int] = Field(None, description="ID of the related diagnosis")
    ordered_date: datetime = Field(..., description="Date when the procedure was ordered")
    priority: int = Field(default=3, ge=1, le=5, description="Priority level from 1 (urgent) to 5 (routine)")
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class PatientProcedureCreate(BaseModel):
    """Model for creating a new patient procedure."""
    patient_id: int
    cpt_code_id: int
    diagnosis_id: Optional[int] = None
    ordered_date: datetime
    priority: int = 3
    notes: Optional[str] = None