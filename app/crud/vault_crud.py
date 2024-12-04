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

def get_vaults(db: Session, skip: int = 0, limit: int = 100, location: str = None):
    query = db.query(vault_model.Vault)

    if location:
        query = query.filter(vault_model.Vault.location == location)

    vaults = query.offset(skip).limit(limit).all()


    return vaults

def get_vault(db: Session, vault_id: int):
    return db.query(vault_model.Vault).filter(vault_model.Vault.id == vault_id).first()

def update_vault(db: Session, vault_id: int, vault_update: vault_schema.VaultCreate):
    vault = db.query(vault_model.Vault).filter(vault_model.Vault.id == vault_id).first()
    
    vault.name = vault_update.name
    vault.size = vault_update.size
    vault.capacity = vault_update.capacity
    vault.price_per_hour = vault_update.price_per_hour

    db.commit()
    db.refresh(vault)
    return vault

def delete_vault(db: Session, vault_id: int):
    vault = db.query(vault_model.Vault).filter(vault_model.Vault.id == vault_id).first()
    
    if not vault:
        return False
    
    db.delete(vault)
    db.commit()
    
    return True