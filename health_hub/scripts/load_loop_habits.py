import sqlite3
import sys
from datetime import datetime, date
from sqlalchemy.orm import sessionmaker
from ..db import engine
from ..models import Habit, HabitEntry

def timestamp_to_date(timestamp_ms):
    """Convert Loop Habits timestamp (milliseconds since epoch) to date."""
    return datetime.fromtimestamp(timestamp_ms / 1000).date()

def load_loop_habits_data(loop_habits_db_path):
    """Load data from Loop Habits backup into health_hub database."""
    
    # Create session for health_hub database
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    health_db = SessionLocal()
    
    try:
        # Connect to Loop Habits database
        loop_conn = sqlite3.connect(loop_habits_db_path)
        loop_cursor = loop_conn.cursor()
        
        print("Loading habits...")
        
        # Load habits
        loop_cursor.execute("""
            SELECT id, name, description, archived, unit, target_value, uuid 
            FROM Habits
        """)
        
        habits_data = loop_cursor.fetchall()
        habit_id_mapping = {}
        
        for habit_data in habits_data:
            loop_id, name, description, archived, unit, target_value, uuid = habit_data
            
            # Check if habit already exists
            existing_habit = health_db.query(Habit).filter(Habit.uuid == uuid).first()
            if existing_habit:
                print(f"  Habit '{name}' already exists, skipping...")
                habit_id_mapping[loop_id] = existing_habit.id
                continue
            
            # Create new habit
            habit = Habit(
                name=name,
                description=description,
                archived=bool(archived),
                unit=unit,
                target_value=target_value,
                uuid=uuid
            )
            
            health_db.add(habit)
            health_db.flush()  # Get the ID
            habit_id_mapping[loop_id] = habit.id
            print(f"  Added habit: {name}")
        
        health_db.commit()
        print(f"Loaded {len(habits_data)} habits")
        
        print("\nLoading habit entries...")
        
        # Load repetitions (habit entries)
        loop_cursor.execute("""
            SELECT habit, timestamp, value, notes 
            FROM Repetitions
        """)
        
        repetitions_data = loop_cursor.fetchall()
        entries_added = 0
        
        for rep_data in repetitions_data:
            habit_loop_id, timestamp_ms, value, notes = rep_data
            
            # Skip if we don't have this habit mapped
            if habit_loop_id not in habit_id_mapping:
                continue
            
            habit_id = habit_id_mapping[habit_loop_id]
            entry_date = timestamp_to_date(timestamp_ms)
            
            # Check if entry already exists
            existing_entry = health_db.query(HabitEntry).filter(
                HabitEntry.habit_id == habit_id,
                HabitEntry.date == entry_date
            ).first()
            
            if existing_entry:
                continue
            
            # Create new entry
            entry = HabitEntry(
                habit_id=habit_id,
                date=entry_date,
                value=value,
                notes=notes
            )
            
            health_db.add(entry)
            entries_added += 1
        
        health_db.commit()
        print(f"Loaded {entries_added} habit entries")
        
        loop_conn.close()
        
    except Exception as e:
        health_db.rollback()
        print(f"Error loading data: {e}")
        raise
    finally:
        health_db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python load_loop_habits.py <path_to_loop_habits_backup.db>")
        sys.exit(1)
    
    loop_habits_db_path = sys.argv[1]
    load_loop_habits_data(loop_habits_db_path)