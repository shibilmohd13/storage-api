# app/crud/vault_crud.py
from sqlalchemy.orm import Session
from app.models import vault_model
from app.schemas import vault_schema

def create_vault(db: Session, vault: vault_schema.VaultCreate):
    db_vault = vault_model.Vault(**vault.dict())
    db.add(db_vault)
    db.commit()
    db.refresh(db_vault)
    return db_vault

def get_vaults(db: Session, skip: int = 0, limit: int = 100):
    return db.query(vault_model.Vault).offset(skip).limit(limit).all()

def get_vault(db: Session, vault_id: int):
    return db.query(vault_model.Vault).filter(vault_model.Vault.id == vault_id).first()