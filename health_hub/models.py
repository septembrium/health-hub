from sqlalchemy import Column, Integer, String, Float, Date, Text, Boolean
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

class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    archived = Column(Boolean, default=False)
    unit = Column(String, nullable=True)
    target_value = Column(Float, nullable=True)
    uuid = Column(String, nullable=False, unique=True)

class HabitEntry(Base):
    __tablename__ = "habit_entries"
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    value = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
