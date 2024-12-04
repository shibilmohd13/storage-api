# app/schemas/vault_schema.py
from pydantic import BaseModel, Field
from app.models.vault_model import VaultSize

class VaultBase(BaseModel):
    name: str
    size: VaultSize
    capacity: int
    price_per_hour: float
    location: str

class VaultCreate(VaultBase):
    pass

class Vault(VaultBase):
    id: int

    class Config:
        orm_mode = True