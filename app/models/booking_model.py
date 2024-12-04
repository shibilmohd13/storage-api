# app/models/booking_model.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    vault_id = Column(Integer, ForeignKey("vaults.id"), nullable=False)
    storage_id = Column(Integer, ForeignKey("storages.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    total_price = Column(Float, nullable=False)

    # Relationships
    vault = relationship("Vault", back_populates="bookings")
    storage = relationship("Storage", back_populates="bookings")