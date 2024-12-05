# app/crud/booking_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models import booking_model, storage_model
from app.schemas import booking_schema
from datetime import datetime

def check_storage_availability(db: Session, storage_id: int, start_time: datetime, end_time: datetime):
    # Check for conflicting bookings excluding canceled ones
    conflicting_bookings = db.query(booking_model.Booking).filter(
        booking_model.Booking.storage_id == storage_id,
        booking_model.Booking.is_canceled == False,  # Ignore canceled bookings
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
    ).all()
    
    return len(conflicting_bookings) == 0


def calculate_total_price(db: Session, vault_id: int, start_time: datetime, end_time: datetime):
    # Fetch the vault to get hourly price
    from app.crud.vault_crud import get_vault
    
    vault = get_vault(db, vault_id)
    if not vault:
        raise ValueError("Vault not found")
    
    # Calculate total hours
    duration = (end_time - start_time).total_seconds() / 3600
    
    # Calculate total price
    total_price = vault.price_per_hour * duration
    
    return round(total_price, 2)

def create_booking(db: Session, booking: booking_schema.BookingCreate):
    # Check storage availability
    if not check_storage_availability(db, booking.storage_id, booking.start_time, booking.end_time):
        raise ValueError("Storage is not available for the selected time range")
    
    # Calculate total price
    total_price = calculate_total_price(
        db, 
        booking.vault_id, 
        booking.start_time, 
        booking.end_time
    )
    
    # Create booking model instance
    db_booking = booking_model.Booking(
        vault_id=booking.vault_id,
        storage_id=booking.storage_id,
        start_time=booking.start_time,
        end_time=booking.end_time,
        total_price=total_price,
        is_canceled=False  # Ensure the new booking is not marked as canceled
    )
    
    # Update storage availability
    storage = db.query(storage_model.Storage).filter(
        storage_model.Storage.id == booking.storage_id
    ).first()
    
    if not storage:
        raise ValueError("Storage not found")
    
    storage.is_available = False
    
    # Commit the changes
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    return db_booking


def get_bookings(db: Session, skip: int = 0, limit: int = 100, include_canceled: bool = False):
    query = db.query(booking_model.Booking)
    
    if not include_canceled:
        query = query.filter(booking_model.Booking.is_canceled == False)
    
    return query.offset(skip).limit(limit).all()

def get_booking(db: Session, booking_id: int):
    return db.query(booking_model.Booking).filter(
        booking_model.Booking.id == booking_id
    ).first()

def delete_booking(db: Session, booking_id: int):
    booking = db.query(booking_model.Booking).filter(
        booking_model.Booking.id == booking_id
    ).first()
    
    if not booking:
        return False
    
    # Make storage available only if the booking was not canceled
    if not booking.is_canceled:
        storage = db.query(storage_model.Storage).filter(
            storage_model.Storage.id == booking.storage_id
        ).first()
        if storage:
            storage.is_available = True
    
    db.delete(booking)
    db.commit()
    return True



def update_booking(db: Session, booking_id: int, booking_update: booking_schema.BookingCreate):
    # Fetch the existing booking
    existing_booking = db.query(booking_model.Booking).filter(
        booking_model.Booking.id == booking_id
    ).first()
    
    if not existing_booking:
        raise ValueError("Booking not found")
    
    if existing_booking.is_canceled:
        raise ValueError("Cannot update a canceled booking")
    
    # Check if the new storage is available
    if booking_update.storage_id != existing_booking.storage_id:
        is_available = check_storage_availability(
            db, 
            booking_update.storage_id, 
            booking_update.start_time, 
            booking_update.end_time
        )
        
        if not is_available:
            raise ValueError("Selected storage is not available for the specified time range")
        
        # Update previous storage availability
        prev_storage = db.query(storage_model.Storage).filter(
            storage_model.Storage.id == existing_booking.storage_id
        ).first()
        if prev_storage:
            prev_storage.is_available = True
        
        # Update new storage availability
        new_storage = db.query(storage_model.Storage).filter(
            storage_model.Storage.id == booking_update.storage_id
        ).first()
        if new_storage:
            new_storage.is_available = False
    
    # Calculate new total price
    total_price = calculate_total_price(
        db, 
        booking_update.vault_id, 
        booking_update.start_time, 
        booking_update.end_time
    )
    
    # Update booking details
    existing_booking.vault_id = booking_update.vault_id
    existing_booking.storage_id = booking_update.storage_id
    existing_booking.start_time = booking_update.start_time
    existing_booking.end_time = booking_update.end_time
    existing_booking.total_price = total_price
    
    # Commit changes
    db.commit()
    db.refresh(existing_booking)
    
    return existing_booking



def cancel_booking(db: Session, booking_id: int):
    # Fetch the booking
    booking = db.query(booking_model.Booking).filter(
        booking_model.Booking.id == booking_id
    ).first()
    
    if not booking:
        raise ValueError("Booking not found")
    
    if booking.is_canceled:
        raise ValueError("Booking is already canceled")
    
    # Mark as canceled
    booking.is_canceled = True
    
    # Update storage availability
    storage = db.query(storage_model.Storage).filter(
        storage_model.Storage.id == booking.storage_id
    ).first()
    
    if storage:
        storage.is_available = True
    
    # Commit changes
    db.commit()
    db.refresh(booking)
    
    return booking
