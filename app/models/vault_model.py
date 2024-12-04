# app/models/vault_model.py
from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class VaultSize(enum.Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class Vault(Base):
    __tablename__ = "vaults"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    size = Column(Enum(VaultSize), nullable=False)
    capacity = Column(Integer, nullable=False)
    price_per_hour = Column(Float, nullable=False)
    location = Column(String(length=255), default='Trivandrum', nullable=False) 


    # Relationship with Storage
    storages = relationship("Storage", back_populates="vault")
    # Relationship with Bookings
    bookings = relationship("Booking", back_populates="vault")  