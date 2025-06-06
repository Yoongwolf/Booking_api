from models import Class
from database import SessionLocal
from datetime import datetime
import pytz

def seed_data():
    db = SessionLocal()
    if db.query(Class).count() == 0:
        ist = pytz.timezone('Asia/Kolkata')
        classes = [
            Class(
                name="Yoga",
                datetime=ist.localize(datetime(2025, 6, 7, 10, 0)).astimezone(pytz.utc),
                instructor="Alice",
                total_slots=10,
                available_slots=10
            ),
            Class(
                name="Zumba",
                datetime=ist.localize(datetime(2025, 6, 8, 14, 0)).astimezone(pytz.utc),
                instructor="Bob",
                total_slots=15,
                available_slots=15
            ),
            Class(
                name="HIIT",
                datetime=ist.localize(datetime(2025, 6, 9, 9, 0)).astimezone(pytz.utc),
                instructor="Charlie",
                total_slots=20,
                available_slots=20
            ),
        ]
        db.add_all(classes)
        db.commit()
    db.close()