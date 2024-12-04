# app/api/vault_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.response import ResponseModel
from app.database import get_db
from app.schemas import vault_schema
from app.crud import vault_crud

router = APIRouter()

@router.post("/", response_model=ResponseModel)
def create_vault(vault: vault_schema.VaultCreate, db: Session = Depends(get_db)):
    created_vault = vault_crud.create_vault(db=db, vault=vault)
    return ResponseModel(code=201, message="Vault Created Successfully", data=created_vault) 

@router.get("/", response_model=ResponseModel)
def read_vaults(skip: int = 0, limit: int = 100, location: Optional[str] = None, db: Session = Depends(get_db)):
    vaults = vault_crud.get_vaults(db, skip=skip, limit=limit, location=location)
    return ResponseModel(code=200, message="Vault Fetched Successfully", data=vaults) 

@router.get("/{vault_id}", response_model=ResponseModel)
def read_vault(vault_id: int, db: Session = Depends(get_db)):
    db_vault = vault_crud.get_vault(db, vault_id=vault_id)
    if db_vault is None:
        raise HTTPException(status_code=404, detail="Vault not found")
    return ResponseModel(code=200, message="Vault Fetched Successfully", data=db_vault) 

