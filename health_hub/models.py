from sqlalchemy import Column, Integer, String, Float, Date
from .db import Base

class ResistanceSet(Base):
    __tablename__ = "resistance_sets"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    exercise = Column(String, nullable=False)
    category = Column(String, nullable=False)
    weight = Column(Float, nullable=True)
    weight_unit = Column(String, nullable=True)
    reps = Column(Integer, nullable=True)

class CardioSession(Base):
    __tablename__ = "cardio_sessions"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    exercise = Column(String, nullable=False)
    category = Column(String, nullable=False)
    distance = Column(Float, nullable=True)
    distance_unit = Column(String, nullable=True)
    time = Column(String, nullable=True)
