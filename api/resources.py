from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Resource as ResourceModel, TimeSlot as TimeSlotModel
from models.scheduling import Resource, ResourceCreate, TimeSlot, TimeSlotCreate

router = APIRouter(
    prefix="/resources",
    tags=["resources"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Resource)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    """
    Create a new resource (room, equipment, etc.).
    """
    db_resource = ResourceModel(
        name=resource.name,
        type=resource.type,
        is_available=resource.is_available
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


@router.get("/", response_model=List[Resource])
def read_resources(
    skip: int = 0, 
    limit: int = 100, 
    type: Optional[str] = Query(None, description="Filter by resource type"),
    available: Optional[bool] = Query(None, description="Filter by availability"),
    db: Session = Depends(get_db)
):
    """
    Retrieve resources with optional filtering.
    """
    query = db.query(ResourceModel)
    
    if type:
        query = query.filter(ResourceModel.type == type)
    
    if available is not None:
        query = query.filter(ResourceModel.is_available == available)
    
    resources = query.offset(skip).limit(limit).all()
    return resources


@router.get("/{resource_id}", response_model=Resource)
def read_resource(resource_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific resource by ID.
    """
    resource = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@router.put("/{resource_id}", response_model=Resource)
def update_resource(resource_id: int, resource: ResourceCreate, db: Session = Depends(get_db)):
    """
    Update a resource's information.
    """
    db_resource = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db_resource.name = resource.name
    db_resource.type = resource.type
    db_resource.is_available = resource.is_available
    
    db.commit()
    db.refresh(db_resource)
    return db_resource


@router.delete("/{resource_id}", response_model=dict)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    """
    Delete a resource.
    """
    db_resource = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db.delete(db_resource)
    db.commit()
    return {"message": f"Resource {resource_id} deleted successfully"}


# Time Slots endpoints
@router.post("/{resource_id}/time-slots/", response_model=TimeSlot)
def create_time_slot(
    resource_id: int, 
    time_slot: TimeSlotCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new time slot for a specific resource.
    """
    # Check if resource exists
    resource = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # Create time slot
    db_time_slot = TimeSlotModel(
        resource_id=resource_id,
        date=time_slot.date,
        start_time=time_slot.start_time,
        end_time=time_slot.end_time,
        is_available=time_slot.is_available
    )
    db.add(db_time_slot)
    db.commit()
    db.refresh(db_time_slot)
    return db_time_slot


@router.get("/{resource_id}/time-slots/", response_model=List[TimeSlot])
def read_time_slots(
    resource_id: int,
    skip: int = 0, 
    limit: int = 100, 
    available: Optional[bool] = Query(None, description="Filter by availability"),
    db: Session = Depends(get_db)
):
    """
    Retrieve time slots for a specific resource with optional filtering.
    """
    # Check if resource exists
    resource = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # Query time slots
    query = db.query(TimeSlotModel).filter(TimeSlotModel.resource_id == resource_id)
    
    if available is not None:
        query = query.filter(TimeSlotModel.is_available == available)
    
    time_slots = query.offset(skip).limit(limit).all()
    return time_slots


@router.get("/time-slots/{time_slot_id}", response_model=TimeSlot)
def read_time_slot(time_slot_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific time slot by ID.
    """
    time_slot = db.query(TimeSlotModel).filter(TimeSlotModel.id == time_slot_id).first()
    if time_slot is None:
        raise HTTPException(status_code=404, detail="Time slot not found")
    return time_slot


@router.put("/time-slots/{time_slot_id}", response_model=TimeSlot)
def update_time_slot(time_slot_id: int, time_slot: TimeSlotCreate, db: Session = Depends(get_db)):
    """
    Update a time slot's information.
    """
    db_time_slot = db.query(TimeSlotModel).filter(TimeSlotModel.id == time_slot_id).first()
    if db_time_slot is None:
        raise HTTPException(status_code=404, detail="Time slot not found")
    
    db_time_slot.resource_id = time_slot.resource_id
    db_time_slot.date = time_slot.date
    db_time_slot.start_time = time_slot.start_time
    db_time_slot.end_time = time_slot.end_time
    db_time_slot.is_available = time_slot.is_available
    
    db.commit()
    db.refresh(db_time_slot)
    return db_time_slot


@router.delete("/time-slots/{time_slot_id}", response_model=dict)
def delete_time_slot(time_slot_id: int, db: Session = Depends(get_db)):
    """
    Delete a time slot.
    """
    db_time_slot = db.query(TimeSlotModel).filter(TimeSlotModel.id == time_slot_id).first()
    if db_time_slot is None:
        raise HTTPException(status_code=404, detail="Time slot not found")
    
    db.delete(db_time_slot)
    db.commit()
    return {"message": f"Time slot {time_slot_id} deleted successfully"}