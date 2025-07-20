from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, db
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/api/cardio", tags=["cardio"])

class CardioSessionBase(BaseModel):
    date: date
    exercise: str
    category: str
    distance: float | None = None
    distance_unit: str | None = None
    time: str | None = None

class CardioSessionCreate(CardioSessionBase):
    pass

class CardioSessionRead(CardioSessionBase):
    id: int
    class Config:
        orm_mode = True

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/", response_model=CardioSessionRead)
def create_cardio_session(item: CardioSessionCreate, db: Session = Depends(get_db)):
    db_item = models.CardioSession(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[CardioSessionRead])
def read_cardio_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.CardioSession).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=CardioSessionRead)
def read_cardio_session(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.CardioSession).filter(models.CardioSession.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=CardioSessionRead)
def update_cardio_session(item_id: int, item: CardioSessionCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.CardioSession).filter(models.CardioSession.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_cardio_session(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.CardioSession).filter(models.CardioSession.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"ok": True}
