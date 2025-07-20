import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from health_hub.db import SessionLocal, Base, engine
from health_hub.models import ResistanceSet, CardioSession

load_dotenv()

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None

def main():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    if len(sys.argv) < 2:
        print("Usage: python load_fitnotes_csv.py <fitnotes_export.csv>")
        sys.exit(1)
    csv_path = sys.argv[1]
    df = pd.read_csv(csv_path)
    db: Session = SessionLocal()
    for _, row in df.iterrows():
        date = parse_date(row.get("Date"))
        exercise = row.get("Exercise")
        category = row.get("Category")
        if category == "Cardio":
            session = CardioSession(
                date=date,
                exercise=exercise,
                category=category,
                distance=row.get("Distance", None),
                distance_unit=row.get("Distance Unit", None),
                time=row.get("Time", None)
            )
            db.add(session)
        else:
            set_ = ResistanceSet(
                date=date,
                exercise=exercise,
                category=category,
                weight=row.get("Weight", None),
                weight_unit=row.get("Weight Unit", None),
                reps=row.get("Reps", None)
            )
            db.add(set_)
    db.commit()
    db.close()
    print("Import complete.")

if __name__ == "__main__":
    main()
