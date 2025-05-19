from datetime import datetime, time, timedelta
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

from models.patient import Patient
from models.medical import PatientProcedure, CPTCode, Diagnosis
from models.scheduling import TimeSlot, Resource, Appointment, ScheduleRequest, ScheduleResponse


class SchedulingService:
    """Service for scheduling patient appointments using ML techniques."""
    
    def __init__(self):
        self.scaler = MinMaxScaler()
    
    def optimize_schedule(
        self,
        procedures: List[PatientProcedure],
        patients: List[Patient],
        diagnoses: List[Diagnosis],
        cpt_codes: List[CPTCode],
        time_slots: List[TimeSlot],
        resources: List[Resource],
        request: ScheduleRequest
    ) -> ScheduleResponse:
        """
        Optimize the schedule based on patient procedures and available time slots.
        
        This uses a combination of:
        1. Feature engineering to create a rich representation of procedures and slots
        2. Similarity matching to find the best slot for each procedure
        3. Priority-based scheduling to handle conflicts
        """
        # Filter procedures based on request parameters
        filtered_procedures = self._filter_procedures(procedures, request)
        
        if not filtered_procedures:
            return ScheduleResponse(
                appointments=[],
                unscheduled_procedures=[],
                optimization_score=0.0,
                message="No procedures to schedule"
            )
        
        # Filter time slots based on date range and availability
        filtered_slots = self._filter_time_slots(time_slots, request)
        
        if not filtered_slots:
            return ScheduleResponse(
                appointments=[],
                unscheduled_procedures=[p.id for p in filtered_procedures],
                optimization_score=0.0,
                message="No available time slots in the specified date range"
            )
        
        # Create feature matrices for procedures and slots
        procedure_features = self._create_procedure_features(filtered_procedures, patients, diagnoses, cpt_codes)
        slot_features = self._create_slot_features(filtered_slots, resources)
        
        # Normalize features
        procedure_features_norm = self.scaler.fit_transform(procedure_features)
        slot_features_norm = self.scaler.transform(slot_features)
        
        # Calculate similarity between procedures and slots
        similarity_matrix = cosine_similarity(procedure_features_norm, slot_features_norm)
        
        # Assign procedures to slots based on similarity and constraints
        appointments, unscheduled = self._assign_procedures_to_slots(
            filtered_procedures, filtered_slots, similarity_matrix, cpt_codes, resources
        )
        
        # Calculate optimization score
        optimization_score = self._calculate_optimization_score(appointments, unscheduled, filtered_procedures)
        
        return ScheduleResponse(
            appointments=appointments,
            unscheduled_procedures=[p.id for p in unscheduled],
            optimization_score=optimization_score,
            message=f"Scheduled {len(appointments)} out of {len(filtered_procedures)} procedures"
        )
    
    def _filter_procedures(self, procedures: List[PatientProcedure], request: ScheduleRequest) -> List[PatientProcedure]:
        """Filter procedures based on request parameters."""
        filtered = procedures.copy()
        
        # Filter by patient IDs if specified
        if request.patient_ids:
            filtered = [p for p in filtered if p.patient_id in request.patient_ids]
        
        # Filter by procedure IDs if specified
        if request.procedure_ids:
            filtered = [p for p in filtered if p.id in request.procedure_ids]
        
        # Filter by priority threshold if specified
        if request.priority_threshold is not None:
            filtered = [p for p in filtered if p.priority <= request.priority_threshold]
        
        # Sort by priority (lower number = higher priority)
        filtered.sort(key=lambda p: p.priority)
        
        return filtered
    
    def _filter_time_slots(self, time_slots: List[TimeSlot], request: ScheduleRequest) -> List[TimeSlot]:
        """Filter time slots based on date range and availability."""
        return [
            slot for slot in time_slots
            if slot.is_available and
               request.start_date <= slot.date <= request.end_date
        ]
    
    def _create_procedure_features(
        self, 
        procedures: List[PatientProcedure], 
        patients: List[Patient],
        diagnoses: List[Diagnosis],
        cpt_codes: List[CPTCode]
    ) -> np.ndarray:
        """Create feature matrix for procedures."""
        # Create dictionaries for quick lookup
        patient_dict = {p.id: p for p in patients}
        diagnosis_dict = {d.id: d for d in diagnoses}
        cpt_dict = {c.id: c for c in cpt_codes}
        
        features = []
        for proc in procedures:
            patient = patient_dict.get(proc.patient_id)
            diagnosis = diagnosis_dict.get(proc.diagnosis_id) if proc.diagnosis_id else None
            cpt = cpt_dict.get(proc.cpt_code_id)
            
            # Calculate patient age
            age = (datetime.now().date() - patient.date_of_birth.date()).days / 365.25 if patient else 0
            
            # Create feature vector
            feature_vector = [
                proc.priority,  # Priority (1-5)
                cpt.duration_minutes if cpt else 30,  # Duration
                1 if cpt and cpt.requires_specialist else 0,  # Requires specialist
                diagnosis.severity if diagnosis else 3,  # Diagnosis severity
                age,  # Patient age
                (datetime.now() - proc.ordered_date).days,  # Days since ordered
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def _create_slot_features(self, slots: List[TimeSlot], resources: List[Resource]) -> np.ndarray:
        """Create feature matrix for time slots."""
        # Create dictionary for quick lookup
        resource_dict = {r.id: r for r in resources}
        
        features = []
        for slot in slots:
            resource = resource_dict.get(slot.resource_id)
            
            # Calculate slot duration in minutes
            start_datetime = datetime.combine(slot.date.date(), slot.start_time)
            end_datetime = datetime.combine(slot.date.date(), slot.end_time)
            duration = (end_datetime - start_datetime).total_seconds() / 60
            
            # Calculate days from now
            days_from_now = (slot.date.date() - datetime.now().date()).days
            
            # Calculate time of day (0-24 scale, where 0 is midnight)
            time_of_day = slot.start_time.hour + slot.start_time.minute / 60
            
            # Create feature vector
            feature_vector = [
                3,  # Neutral priority
                duration,  # Duration in minutes
                1 if resource and resource.type in ["Procedure Room", "X-Ray Room", "EKG Room"] else 0,  # Specialist room
                3,  # Neutral severity
                50,  # Neutral age
                days_from_now,  # Days from now
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def _assign_procedures_to_slots(
        self,
        procedures: List[PatientProcedure],
        slots: List[TimeSlot],
        similarity_matrix: np.ndarray,
        cpt_codes: List[CPTCode],
        resources: List[Resource]
    ) -> Tuple[List[Appointment], List[PatientProcedure]]:
        """Assign procedures to slots based on similarity and constraints."""
        # Create dictionaries for quick lookup
        cpt_dict = {c.id: c for c in cpt_codes}
        resource_dict = {r.id: r for r in resources}
        
        # Track which slots are already assigned
        assigned_slots = set()
        
        appointments = []
        unscheduled_procedures = []
        
        for i, procedure in enumerate(procedures):
            # Get the CPT code for this procedure
            cpt = cpt_dict.get(procedure.cpt_code_id)
            if not cpt:
                unscheduled_procedures.append(procedure)
                continue
            
            # Get the procedure duration
            duration_minutes = cpt.duration_minutes
            
            # Get similarity scores for this procedure
            similarity_scores = similarity_matrix[i]
            
            # Sort slots by similarity score (highest first)
            sorted_indices = np.argsort(-similarity_scores)
            
            assigned = False
            for idx in sorted_indices:
                slot = slots[idx]
                
                # Skip if slot is already assigned
                if slot.id in assigned_slots:
                    continue
                
                # Check if the slot duration is sufficient
                slot_start = datetime.combine(slot.date.date(), slot.start_time)
                slot_end = datetime.combine(slot.date.date(), slot.end_time)
                slot_duration = (slot_end - slot_start).total_seconds() / 60
                
                if slot_duration < duration_minutes:
                    continue
                
                # Check if the resource is appropriate for the procedure
                resource = resource_dict.get(slot.resource_id)
                if cpt.requires_specialist and resource.type not in ["Procedure Room", "X-Ray Room", "EKG Room"]:
                    continue
                
                # Create appointment
                appointment = Appointment(
                    id=len(appointments) + 1,  # Generate a new ID
                    patient_id=procedure.patient_id,
                    procedure_id=procedure.id,
                    resource_id=slot.resource_id,
                    scheduled_date=slot.date,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    status="scheduled",
                    notes=f"Automatically scheduled by AI algorithm",
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                appointments.append(appointment)
                assigned_slots.add(slot.id)
                assigned = True
                break
            
            if not assigned:
                unscheduled_procedures.append(procedure)
        
        return appointments, unscheduled_procedures
    
    def _calculate_optimization_score(
        self,
        appointments: List[Appointment],
        unscheduled: List[PatientProcedure],
        all_procedures: List[PatientProcedure]
    ) -> float:
        """Calculate a score for how optimal the schedule is."""
        if not all_procedures:
            return 0.0
        
        # Basic score based on percentage of scheduled procedures
        scheduling_rate = len(appointments) / len(all_procedures)
        
        # Penalty for high-priority unscheduled procedures
        priority_penalty = sum(1 / p.priority for p in unscheduled) / len(all_procedures) if unscheduled else 0
        
        # Final score (0-1 scale)
        score = scheduling_rate - 0.2 * priority_penalty
        
        return max(0, min(1, score))  # Clamp to 0-1 range