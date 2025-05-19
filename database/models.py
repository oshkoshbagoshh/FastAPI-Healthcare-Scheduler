from datetime import datetime, time
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Time, ForeignKey, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Patient(Base):
    """SQLAlchemy model for patients."""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    insurance_provider = Column(String, nullable=True)
    insurance_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    diagnoses = relationship("PatientDiagnosis", back_populates="patient")
    procedures = relationship("PatientProcedure", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")


class Diagnosis(Base):
    """SQLAlchemy model for diagnoses."""
    __tablename__ = "diagnoses"
    
    id = Column(Integer, primary_key=True, index=True)
    icd_code = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    severity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    patient_diagnoses = relationship("PatientDiagnosis", back_populates="diagnosis")


class CPTCode(Base):
    """SQLAlchemy model for CPT codes."""
    __tablename__ = "cpt_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    requires_specialist = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    patient_procedures = relationship("PatientProcedure", back_populates="cpt_code")


class PatientDiagnosis(Base):
    """SQLAlchemy model for patient diagnoses."""
    __tablename__ = "patient_diagnoses"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    diagnosis_id = Column(Integer, ForeignKey("diagnoses.id"), nullable=False)
    diagnosed_date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    patient = relationship("Patient", back_populates="diagnoses")
    diagnosis = relationship("Diagnosis", back_populates="patient_diagnoses")


class PatientProcedure(Base):
    """SQLAlchemy model for patient procedures."""
    __tablename__ = "patient_procedures"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    cpt_code_id = Column(Integer, ForeignKey("cpt_codes.id"), nullable=False)
    diagnosis_id = Column(Integer, ForeignKey("diagnoses.id"), nullable=True)
    ordered_date = Column(DateTime, nullable=False)
    priority = Column(Integer, default=3)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    patient = relationship("Patient", back_populates="procedures")
    cpt_code = relationship("CPTCode", back_populates="patient_procedures")
    diagnosis = relationship("Diagnosis")
    appointments = relationship("Appointment", back_populates="procedure")


class Resource(Base):
    """SQLAlchemy model for resources."""
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    time_slots = relationship("TimeSlot", back_populates="resource")
    appointments = relationship("Appointment", back_populates="resource")


class TimeSlot(Base):
    """SQLAlchemy model for time slots."""
    __tablename__ = "time_slots"
    
    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    resource = relationship("Resource", back_populates="time_slots")


class Appointment(Base):
    """SQLAlchemy model for appointments."""
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    procedure_id = Column(Integer, ForeignKey("patient_procedures.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String, default="scheduled")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    procedure = relationship("PatientProcedure", back_populates="appointments")
    resource = relationship("Resource", back_populates="appointments")