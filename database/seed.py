from sqlalchemy.orm import Session
from typing import Dict, Any, List

from database.models import Patient, Diagnosis, CPTCode, PatientDiagnosis, PatientProcedure, Resource, TimeSlot
from utils.data_generator import generate_all_data


def seed_database(db: Session, patient_count: int = 50, resource_count: int = 10, days_ahead: int = 30) -> Dict[str, int]:
    """
    Seed the database with fake data.
    
    Args:
        db: Database session
        patient_count: Number of patients to generate
        resource_count: Number of resources to generate
        days_ahead: Number of days ahead to generate time slots for
        
    Returns:
        Dict with counts of created records
    """
    # Generate all data
    data = generate_all_data(patient_count, resource_count, days_ahead)
    
    # Seed patients
    patients = []
    for patient_data in data["patients"]:
        patient = Patient(
            first_name=patient_data.first_name,
            last_name=patient_data.last_name,
            date_of_birth=patient_data.date_of_birth,
            gender=patient_data.gender,
            phone_number=patient_data.phone_number,
            email=patient_data.email,
            address=patient_data.address,
            insurance_provider=patient_data.insurance_provider,
            insurance_id=patient_data.insurance_id
        )
        patients.append(patient)
    
    db.add_all(patients)
    db.commit()
    
    # Seed diagnoses
    diagnoses = []
    for diagnosis_data in data["diagnoses"]:
        diagnosis = Diagnosis(
            icd_code=diagnosis_data.icd_code,
            description=diagnosis_data.description,
            severity=diagnosis_data.severity
        )
        diagnoses.append(diagnosis)
    
    db.add_all(diagnoses)
    db.commit()
    
    # Seed CPT codes
    cpt_codes = []
    for cpt_data in data["cpt_codes"]:
        cpt_code = CPTCode(
            code=cpt_data.code,
            description=cpt_data.description,
            duration_minutes=cpt_data.duration_minutes,
            requires_specialist=cpt_data.requires_specialist
        )
        cpt_codes.append(cpt_code)
    
    db.add_all(cpt_codes)
    db.commit()
    
    # Seed resources
    resources = []
    for resource_data in data["resources"]:
        resource = Resource(
            name=resource_data.name,
            type=resource_data.type,
            is_available=resource_data.is_available
        )
        resources.append(resource)
    
    db.add_all(resources)
    db.commit()
    
    # Seed patient diagnoses
    patient_diagnoses = []
    for pd_data in data["patient_diagnoses"]:
        patient_diagnosis = PatientDiagnosis(
            patient_id=pd_data.patient_id,
            diagnosis_id=pd_data.diagnosis_id,
            diagnosed_date=pd_data.diagnosed_date,
            notes=pd_data.notes
        )
        patient_diagnoses.append(patient_diagnosis)
    
    db.add_all(patient_diagnoses)
    db.commit()
    
    # Seed patient procedures
    patient_procedures = []
    for pp_data in data["patient_procedures"]:
        patient_procedure = PatientProcedure(
            patient_id=pp_data.patient_id,
            cpt_code_id=pp_data.cpt_code_id,
            diagnosis_id=pp_data.diagnosis_id,
            ordered_date=pp_data.ordered_date,
            priority=pp_data.priority,
            notes=pp_data.notes
        )
        patient_procedures.append(patient_procedure)
    
    db.add_all(patient_procedures)
    db.commit()
    
    # Seed time slots
    time_slots = []
    for ts_data in data["time_slots"]:
        time_slot = TimeSlot(
            resource_id=ts_data.resource_id,
            date=ts_data.date,
            start_time=ts_data.start_time,
            end_time=ts_data.end_time,
            is_available=ts_data.is_available
        )
        time_slots.append(time_slot)
    
    db.add_all(time_slots)
    db.commit()
    
    # Return counts
    return {
        "patients": len(patients),
        "diagnoses": len(diagnoses),
        "cpt_codes": len(cpt_codes),
        "resources": len(resources),
        "patient_diagnoses": len(patient_diagnoses),
        "patient_procedures": len(patient_procedures),
        "time_slots": len(time_slots)
    }