from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, db
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/api/resistance", tags=["resistance"])

class ResistanceSetBase(BaseModel):
    date: date
    exercise: str
    category: str
    weight: float | None = None
    weight_unit: str | None = None
    reps: int | None = None

class ResistanceSetCreate(ResistanceSetBase):
    pass

class ResistanceSetRead(ResistanceSetBase):
    id: int
    class Config:
        orm_mode = True

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/", response_model=ResistanceSetRead)
def create_resistance_set(item: ResistanceSetCreate, db: Session = Depends(get_db)):
    db_item = models.ResistanceSet(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[ResistanceSetRead])
def read_resistance_sets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ResistanceSet).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=ResistanceSetRead)
def read_resistance_set(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.ResistanceSet).filter(models.ResistanceSet.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ResistanceSetRead)
def update_resistance_set(item_id: int, item: ResistanceSetCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.ResistanceSet).filter(models.ResistanceSet.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_resistance_set(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.ResistanceSet).filter(models.ResistanceSet.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"ok": True}
