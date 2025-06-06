from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Class, Booking
from schemas import ClassOut, BookingRequest, BookingOut
from utils import convert_to_timezone
from typing import List
from datetime import datetime
import pytz
from seed_data import seed_data

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Seed initial data
seed_data()

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/classes", response_model=List[ClassOut])
def get_classes(timezone: str = Query("Asia/Kolkata"), db: Session = Depends(get_db)):
    """Get all upcoming classes with details in the specified timezone."""
    now = datetime.utcnow()
    classes = db.query(Class).filter(Class.datetime > now).all()
    result = []
    for cls in classes:
        dt_local = convert_to_timezone(cls.datetime, timezone)
        result.append(ClassOut(
            id=cls.id,
            name=cls.name,
            datetime=dt_local,
            instructor=cls.instructor,
            available_slots=cls.available_slots
        ))
    return result

@app.post("/book")
def book_class(booking: BookingRequest, db: Session = Depends(get_db)):
    """Book a spot in a class."""
    class_ = db.query(Class).filter(Class.id == booking.class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    now = datetime.utcnow()
    if class_.datetime < now:
        raise HTTPException(status_code=400, detail="Cannot book past classes")
    if class_.available_slots <= 0:
        raise HTTPException(status_code=400, detail="Class is fully booked")
    # Check for duplicate booking
    existing_booking = db.query(Booking).filter(
        Booking.class_id == booking.class_id,
        Booking.client_email == booking.client_email
    ).first()
    if existing_booking:
        raise HTTPException(status_code=400, detail="Client has already booked this class")
    # Create new booking and update available slots
    new_booking = Booking(
        class_id=booking.class_id,
        client_name=booking.client_name,
        client_email=booking.client_email
    )
    db.add(new_booking)
    class_.available_slots -= 1
    db.commit()
    return {"message": "Booking successful"}

@app.get("/bookings", response_model=List[BookingOut])
def get_bookings(email: str, timezone: str = Query("Asia/Kolkata"), db: Session = Depends(get_db)):
    """Get all bookings for a specific email with class details in the specified timezone."""
    bookings = db.query(Booking).filter(Booking.client_email == email).all()
    result = []
    for booking in bookings:
        class_ = booking.class_
        dt_local = convert_to_timezone(class_.datetime, timezone)
        result.append(BookingOut(
            class_id=class_.id,
            class_name=class_.name,
            datetime=dt_local,
            instructor=class_.instructor,
            client_name=booking.client_name,
            client_email=booking.client_email
        ))
    return result