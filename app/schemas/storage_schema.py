# app/schemas/storage_schema.py
from pydantic import BaseModel

class StorageBase(BaseModel):
    vault_id: int
    space_number: str
    is_available: bool = True

class StorageCreate(StorageBase):
    pass

class Storage(StorageBase):
    id: int

    class Config:
        orm_mode = True