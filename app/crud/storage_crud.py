# app/crud/storage_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models import storage_model, booking_model, vault_model
from app.schemas import storage_schema
from datetime import datetime

def create_storage(db: Session, storage: storage_schema.StorageCreate):
    # First, verify that the vault exists
    vault = db.query(vault_model.Vault).filter(
        vault_model.Vault.id == storage.vault_id
    ).first()
    
    if not vault:
        raise ValueError(f"Vault with ID {storage.vault_id} does not exist")
    
    # Create the storage
    db_storage = storage_model.Storage(
        vault_id=storage.vault_id,
        space_number=storage.space_number,
        is_available=storage.is_available
    )
    
    db.add(db_storage)
    db.commit()
    db.refresh(db_storage)
    
    return db_storage

def get_storages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(storage_model.Storage).offset(skip).limit(limit).all()

def get_available_storages(
    db: Session, 
    vault_id: int = None, 
    start_time: datetime = None, 
    end_time: datetime = None
):
    # Base query for available storages
    query = db.query(storage_model.Storage).filter(
        storage_model.Storage.is_available == True
    )
    
    # Filter by vault if provided
    if vault_id:
        query = query.filter(storage_model.Storage.vault_id == vault_id)
    
    # If start and end times are provided, check for conflicts
    if start_time and end_time:
        # Subquery to find storages with conflicting bookings
        conflicting_storages = db.query(booking_model.Booking.storage_id).filter(
            or_(
                and_(
                    booking_model.Booking.start_time <= start_time,
                    booking_model.Booking.end_time >= start_time
                ),
                and_(
                    booking_model.Booking.start_time <= end_time,
                    booking_model.Booking.end_time >= end_time
                ),
                and_(
                    booking_model.Booking.start_time >= start_time,
                    booking_model.Booking.end_time <= end_time
                )
            )
        ).subquery()    
        
        # Exclude storages with conflicting bookings
        query = query.filter(
            storage_model.Storage.id.notin_(conflicting_storages)
        )
    
    return query.all()

def get_storage(db: Session, storage_id: int):
    return db.query(storage_model.Storage).filter(storage_model.Storage.id == storage_id).first()