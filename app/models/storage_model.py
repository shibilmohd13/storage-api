# app/models/storage_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Storage(Base):
    __tablename__ = "storages"

    id = Column(Integer, primary_key=True, index=True)
    vault_id = Column(Integer, ForeignKey("vaults.id"), nullable=False)
    space_number = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)
    
    # Relationship with Vault
    vault = relationship("Vault", back_populates="storages")
    # Relationship with Bookings
    bookings = relationship("Booking", back_populates="storage")