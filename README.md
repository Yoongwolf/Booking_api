# Fitness Booking API

## Overview

This is a RESTful API for a fictional fitness studio, built with **Python** and **FastAPI**. It allows clients to view upcoming classes, book a spot, and retrieve their bookings, with support for timezone conversions.

The project uses:
- **SQLite** for data storage
- **SQLAlchemy** for ORM
- **Pydantic** for input validation

This project was created as part of a job assessment for a Python developer role.

---

## Features

### Endpoints

- `GET /classes`: Lists all upcoming classes with name, date/time, instructor, and available slots.
- `POST /book`: Books a spot in a class, validating slot availability and preventing duplicates.
- `GET /bookings`: Retrieves all bookings for a given email.

### Additional Functionality

- **Timezone Handling**: Classes are created in IST, stored in UTC, and displayed in any requested timezone.
- **Error Handling**: Validates inputs and handles edge cases (e.g., non-existent classes, fully booked classes).
- **Seed Data**: Includes three sample classes (Yoga, Zumba, HIIT) for testing.

---

## Project Structure

- `main.py`: Defines FastAPI app and endpoints.
- `models.py`: SQLAlchemy models for database schema.
- `database.py`: SQLite database setup.
- `schemas.py`: Pydantic models for request/response validation.
- `utils.py`: Utility function for timezone conversion.
- `seed_data.py`: Seeds the database with sample classes.
- `requirements.txt`: Lists dependencies.
- `README.md`: This file.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Yoongwolf/Booking_api.git
cd Booking_api
````

### 2. Install Dependencies

Ensure Python 3.8+ is installed, then run:

```bash
python -m pip install -r requirements.txt
```

### 3. Run the Application

```bash
python -m uvicorn main:app --reload
```

The API will be available at:
[http://localhost:8000](http://localhost:8000)

Interactive Swagger UI:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## Sample Requests

### 🔹 GET `/classes`

Lists all upcoming classes in the specified timezone (default: Asia/Kolkata).

**cURL:**

```bash
curl -X GET "http://localhost:8000/classes?timezone=Asia/Kolkata"
```

**Example Response:**

```json
[
  {
    "id": 1,
    "name": "Yoga",
    "datetime": "2025-06-07T10:00:00+05:30",
    "instructor": "Alice",
    "available_slots": 10
  },
  {
    "id": 2,
    "name": "Zumba",
    "datetime": "2025-06-08T14:00:00+05:30",
    "instructor": "Bob",
    "available_slots": 15
  },
  {
    "id": 3,
    "name": "HIIT",
    "datetime": "2025-06-09T09:00:00+05:30",
    "instructor": "Charlie",
    "available_slots": 20
  }
]
```

---

### 🔹 POST `/book`

Books a spot in a class.

**cURL:**

```bash
curl -X POST "http://localhost:8000/book" \
-H "Content-Type: application/json" \
-d '{"class_id": 1, "client_name": "John Doe", "client_email": "john@example.com"}'
```

**Example Response:**

```json
{"message": "Booking successful"}
```

---

### 🔹 GET `/bookings`

Retrieves bookings for a specific email.

**cURL:**

```bash
curl -X GET "http://localhost:8000/bookings?email=john@example.com&timezone=Asia/Kolkata"
```

**Example Response:**

```json
[
  {
    "class_id": 1,
    "class_name": "Yoga",
    "datetime": "2025-06-07T10:00:00+05:30",
    "instructor": "Alice",
    "client_name": "John Doe",
    "client_email": "john@example.com"
  }
]
```

---

## Seed Data

The database is seeded with the following classes:

* **Yoga**: June 7, 2025, 10:00 AM IST, 10 slots, Instructor: Alice
* **Zumba**: June 8, 2025, 2:00 PM IST, 15 slots, Instructor: Bob
* **HIIT**: June 9, 2025, 9:00 AM IST, 20 slots, Instructor: Charlie

---

## Notes

* **Timezone Handling**: Dates are stored in UTC and converted to the requested timezone.
* **Error Handling**: Includes validation for non-existent classes, past classes, fully booked classes, and duplicate bookings.
* **Database**: Uses SQLite (`fitness.db`) for simplicity.

---

## Submission

* **GitHub Repository**: [https://github.com/Yoongwolf/Booking\_api](https://github.com/Yoongwolf/Booking_api)
* **Loom Video**: *\[https://www.loom.com/share/5a588dde859d4a87b43080d519dfbf2b?sid=e7d6259e-ebc5-4705-a0d4-da9b1cce2267)]*
