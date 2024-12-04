# app/api/storage_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.response import ResponseModel
from app.database import get_db
from app.schemas import storage_schema
from app.crud import storage_crud

router = APIRouter()

@router.post("/", response_model=ResponseModel)
def create_storage(storage: storage_schema.StorageCreate, db: Session = Depends(get_db)):
    try:
        created_storage = storage_crud.create_storage(db=db, storage=storage)
        return ResponseModel(code=201, message="Storage Created Successfully", data=created_storage) 
 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=ResponseModel)
def read_storages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    storages = storage_crud.get_storages(db, skip=skip, limit=limit)
    return ResponseModel(code=200, message="Storage Fetched Successfully", data=storages) 

@router.get("/{storage_id}", response_model=ResponseModel)
def read_storage(storage_id: int, db: Session = Depends(get_db)):
    storage = storage_crud.get_storage(db, storage_id)
    if storage is None:
        raise HTTPException(status_code=404, detail="Storage not found")
    return ResponseModel(code=200, message="Storage Fetched Successfully", data=storage) 

@router.put("/{storage_id}", response_model=ResponseModel)
def update_storage(storage_id: int, storage: storage_schema.StorageCreate, db: Session = Depends(get_db)):
    try:
        updated_storage = storage_crud.update_storage(db=db, storage_id=storage_id, storage=storage)
        if updated_storage is None:
            raise HTTPException(status_code=404, detail="Storage not found")
        return ResponseModel(code=200, message="Storage Updated Successfully", data=updated_storage)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{storage_id}", response_model=ResponseModel)
def delete_storage(storage_id: int, db: Session = Depends(get_db)):
    try:
        is_deleted = storage_crud.delete_storage(db=db, storage_id=storage_id)
        if not is_deleted:
            raise HTTPException(status_code=404, detail="Storage not found")
        return ResponseModel(code=200, message="Storage Deleted Successfully", data=None)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

