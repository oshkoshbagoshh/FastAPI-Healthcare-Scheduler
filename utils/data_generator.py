from datetime import datetime, time, timedelta
import random
from typing import List, Dict, Any, Optional
from faker import Faker

from models.patient import PatientCreate
from models.medical import DiagnosisCreate, CPTCodeCreate, PatientDiagnosisCreate, PatientProcedureCreate
from models.scheduling import ResourceCreate, TimeSlotCreate

fake = Faker()

# Sample ICD-10 codes and descriptions for common diagnoses
SAMPLE_DIAGNOSES = [
    {"icd_code": "I10", "description": "Essential (primary) hypertension", "severity": 2},
    {"icd_code": "E11.9", "description": "Type 2 diabetes mellitus without complications", "severity": 3},
    {"icd_code": "J45.909", "description": "Unspecified asthma, uncomplicated", "severity": 3},
    {"icd_code": "M54.5", "description": "Low back pain", "severity": 2},
    {"icd_code": "F41.9", "description": "Anxiety disorder, unspecified", "severity": 2},
    {"icd_code": "F32.9", "description": "Major depressive disorder, single episode, unspecified", "severity": 3},
    {"icd_code": "J02.9", "description": "Acute pharyngitis, unspecified", "severity": 1},
    {"icd_code": "N39.0", "description": "Urinary tract infection, site not specified", "severity": 2},
    {"icd_code": "K21.9", "description": "Gastro-esophageal reflux disease without esophagitis", "severity": 2},
    {"icd_code": "R51", "description": "Headache", "severity": 1},
    {"icd_code": "J06.9", "description": "Acute upper respiratory infection, unspecified", "severity": 1},
    {"icd_code": "H66.90", "description": "Otitis media, unspecified, unspecified ear", "severity": 1},
    {"icd_code": "L30.9", "description": "Dermatitis, unspecified", "severity": 1},
    {"icd_code": "M25.50", "description": "Pain in unspecified joint", "severity": 2},
    {"icd_code": "R10.9", "description": "Unspecified abdominal pain", "severity": 2},
]

# Sample CPT codes and descriptions for common procedures
SAMPLE_CPT_CODES = [
    {"code": "99213", "description": "Office/outpatient visit, established patient, 15 minutes", "duration_minutes": 15, "requires_specialist": False},
    {"code": "99214", "description": "Office/outpatient visit, established patient, 25 minutes", "duration_minutes": 25, "requires_specialist": False},
    {"code": "99215", "description": "Office/outpatient visit, established patient, 40 minutes", "duration_minutes": 40, "requires_specialist": True},
    {"code": "99203", "description": "Office/outpatient visit, new patient, 30 minutes", "duration_minutes": 30, "requires_specialist": False},
    {"code": "99204", "description": "Office/outpatient visit, new patient, 45 minutes", "duration_minutes": 45, "requires_specialist": True},
    {"code": "99205", "description": "Office/outpatient visit, new patient, 60 minutes", "duration_minutes": 60, "requires_specialist": True},
    {"code": "93000", "description": "Electrocardiogram, routine, with interpretation", "duration_minutes": 20, "requires_specialist": False},
    {"code": "71045", "description": "X-ray, chest, single view", "duration_minutes": 15, "requires_specialist": False},
    {"code": "71046", "description": "X-ray, chest, 2 views", "duration_minutes": 20, "requires_specialist": False},
    {"code": "80053", "description": "Comprehensive metabolic panel", "duration_minutes": 10, "requires_specialist": False},
    {"code": "85025", "description": "Complete blood count (CBC)", "duration_minutes": 10, "requires_specialist": False},
    {"code": "82607", "description": "Vitamin B-12 blood test", "duration_minutes": 10, "requires_specialist": False},
    {"code": "83036", "description": "Hemoglobin A1C level", "duration_minutes": 10, "requires_specialist": False},
    {"code": "80061", "description": "Lipid panel", "duration_minutes": 10, "requires_specialist": False},
    {"code": "96372", "description": "Therapeutic, prophylactic, or diagnostic injection", "duration_minutes": 15, "requires_specialist": False},
]

# Sample resource types for outpatient settings
RESOURCE_TYPES = [
    "Exam Room",
    "Procedure Room",
    "X-Ray Room",
    "Lab",
    "EKG Room",
    "Consultation Room",
]


def generate_patients(count: int = 50) -> List[PatientCreate]:
    """Generate a list of fake patients."""
    patients = []
    for _ in range(count):
        gender = random.choice(["Male", "Female", "Other"])
        first_name = fake.first_name_male() if gender == "Male" else fake.first_name_female()
        
        patient = PatientCreate(
            first_name=first_name,
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90),
            gender=gender,
            phone_number=fake.phone_number(),
            email=fake.email(),
            address=fake.address(),
            insurance_provider=fake.company(),
            insurance_id=fake.uuid4()
        )
        patients.append(patient)
    
    return patients


def generate_diagnoses() -> List[DiagnosisCreate]:
    """Generate a list of diagnoses from the sample data."""
    return [DiagnosisCreate(**diagnosis) for diagnosis in SAMPLE_DIAGNOSES]


def generate_cpt_codes() -> List[CPTCodeCreate]:
    """Generate a list of CPT codes from the sample data."""
    return [CPTCodeCreate(**cpt_code) for cpt_code in SAMPLE_CPT_CODES]


def generate_patient_diagnoses(patient_count: int, diagnosis_count: int) -> List[PatientDiagnosisCreate]:
    """Generate patient diagnoses by randomly assigning diagnoses to patients."""
    patient_diagnoses = []
    
    for patient_id in range(1, patient_count + 1):
        # Each patient gets 1-3 diagnoses
        num_diagnoses = random.randint(1, 3)
        diagnosis_ids = random.sample(range(1, diagnosis_count + 1), num_diagnoses)
        
        for diagnosis_id in diagnosis_ids:
            patient_diagnosis = PatientDiagnosisCreate(
                patient_id=patient_id,
                diagnosis_id=diagnosis_id,
                diagnosed_date=fake.date_time_between(start_date="-1y", end_date="now"),
                notes=fake.text(max_nb_chars=100) if random.random() > 0.7 else None
            )
            patient_diagnoses.append(patient_diagnosis)
    
    return patient_diagnoses


def generate_patient_procedures(patient_diagnoses: List[PatientDiagnosisCreate], cpt_code_count: int) -> List[PatientProcedureCreate]:
    """Generate patient procedures based on their diagnoses."""
    patient_procedures = []
    
    for pd in patient_diagnoses:
        # Each diagnosis may lead to 0-2 procedures
        num_procedures = random.randint(0, 2)
        
        for _ in range(num_procedures):
            cpt_code_id = random.randint(1, cpt_code_count)
            priority = random.randint(1, 5)
            
            patient_procedure = PatientProcedureCreate(
                patient_id=pd.patient_id,
                cpt_code_id=cpt_code_id,
                diagnosis_id=pd.diagnosis_id,
                ordered_date=pd.diagnosed_date + timedelta(days=random.randint(1, 14)),
                priority=priority,
                notes=fake.text(max_nb_chars=100) if random.random() > 0.7 else None
            )
            patient_procedures.append(patient_procedure)
    
    return patient_procedures


def generate_resources(count: int = 10) -> List[ResourceCreate]:
    """Generate a list of resources for the outpatient setting."""
    resources = []
    
    for i in range(count):
        resource_type = random.choice(RESOURCE_TYPES)
        resource = ResourceCreate(
            name=f"{resource_type} {i+1}",
            type=resource_type,
            is_available=random.random() > 0.1  # 90% of resources are available
        )
        resources.append(resource)
    
    return resources


def generate_time_slots(resource_count: int, days_ahead: int = 30) -> List[TimeSlotCreate]:
    """Generate available time slots for resources."""
    time_slots = []
    
    # Generate time slots for the next 'days_ahead' days
    for day in range(days_ahead):
        current_date = datetime.now().date() + timedelta(days=day)
        
        # Skip weekends
        if current_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            continue
        
        for resource_id in range(1, resource_count + 1):
            # Generate slots from 8 AM to 5 PM in 30-minute increments
            start_hour = 8
            end_hour = 17
            
            for hour in range(start_hour, end_hour):
                for minute in [0, 30]:
                    start_time = time(hour, minute)
                    end_time = time(hour, minute + 30) if minute == 0 else time(hour + 1, 0)
                    
                    # Convert date to datetime for the model
                    slot_date = datetime.combine(current_date, time(0, 0))
                    
                    time_slot = TimeSlotCreate(
                        resource_id=resource_id,
                        date=slot_date,
                        start_time=start_time,
                        end_time=end_time,
                        is_available=random.random() > 0.2  # 80% of slots are available
                    )
                    time_slots.append(time_slot)
    
    return time_slots


def generate_all_data(
    patient_count: int = 50,
    resource_count: int = 10,
    days_ahead: int = 30
) -> Dict[str, List[Any]]:
    """Generate all data needed for the application."""
    # Generate basic data
    patients = generate_patients(patient_count)
    diagnoses = generate_diagnoses()
    cpt_codes = generate_cpt_codes()
    resources = generate_resources(resource_count)
    
    # Generate relational data
    patient_diagnoses = generate_patient_diagnoses(patient_count, len(diagnoses))
    patient_procedures = generate_patient_procedures(patient_diagnoses, len(cpt_codes))
    time_slots = generate_time_slots(resource_count, days_ahead)
    
    return {
        "patients": patients,
        "diagnoses": diagnoses,
        "cpt_codes": cpt_codes,
        "resources": resources,
        "patient_diagnoses": patient_diagnoses,
        "patient_procedures": patient_procedures,
        "time_slots": time_slots
    }