# app/schemas/booking_schema.py
from pydantic import BaseModel, validator
from datetime import datetime

class BookingBase(BaseModel):
    vault_id: int
    storage_id: int
    start_time: datetime
    end_time: datetime

    @validator("start_time", "end_time", pre=True)
    def format_datetime(cls, value):
        """
        Formats datetime fields to a readable format.
        """
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value

class BookingCreate(BookingBase):
    pass

    @validator("end_time")
    def validate_time(cls, end_time, values):
        start_time = values.get("start_time")
        if start_time and end_time <= start_time:
            raise ValueError("End time must be greater than start time")
        return end_time

class Booking(BookingBase):
    id: int
    total_price: float

    class Config:
        orm_mode = True
