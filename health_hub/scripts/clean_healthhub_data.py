import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from health_hub.db import SessionLocal, Base, engine
from health_hub.models import ResistanceSet, CardioSession

def clean_database():
    db = SessionLocal()
    db.query(ResistanceSet).delete()
    db.query(CardioSession).delete()
    db.commit()
    db.close()
    print("All data deleted from ResistanceSet and CardioSession tables.")

if __name__ == "__main__":
    clean_database()