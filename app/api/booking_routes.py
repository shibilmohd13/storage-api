# app/api/booking_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.response import ResponseModel
from app.database import get_db
from app.schemas import booking_schema
from app.crud import booking_crud

router = APIRouter()

@router.post("/", response_model=ResponseModel)
def create_booking(booking: booking_schema.BookingCreate, db: Session = Depends(get_db)):
    # Check storage availability
    try:
        created_booking = booking_crud.create_booking(db=db, booking=booking)
        return ResponseModel(code=201, message="Booking Created Successfully", data=created_booking) 

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{booking_id}", response_model=ResponseModel)
def update_booking(
    booking_id: int, 
    booking: booking_schema.BookingCreate, 
    db: Session = Depends(get_db)
):
    try:
        updated_booking = booking_crud.update_booking(
            db=db, 
            booking_id=booking_id, 
            booking_update=booking
        )
        return ResponseModel(code=200, message="Updated Booking Successfully", data=updated_booking) 
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=ResponseModel)
def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = booking_crud.get_bookings(db, skip=skip, limit=limit)
    return ResponseModel(code=200, message="Booking Fetched Successfully", data=bookings) 

@router.get("/{booking_id}", response_model=ResponseModel)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = booking_crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return ResponseModel(code=200, message="Booking Fetched Successfully", data=db_booking) 

@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    success = booking_crud.delete_booking(db, booking_id=booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"detail": "Booking deleted successfully"}
# app/api/booking_routes.py

@router.put("/{booking_id}/cancel", response_model=ResponseModel)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        canceled_booking = booking_crud.cancel_booking(db=db, booking_id=booking_id)
        return ResponseModel(
            code=200, 
            message="Booking Canceled Successfully", 
            data=canceled_booking
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

