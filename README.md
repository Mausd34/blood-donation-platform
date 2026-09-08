# Blood Donation Platform

Professional blood donor and emergency request matching platform.

## Features
- Donor registration and blood-group profiles
- Emergency blood requests
- City and blood-group matching
- Availability/status workflow
- REST API with validation
- Privacy-conscious contact workflow

## Stack
Python · FastAPI · Pydantic · Docker

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload
```
Open `http://127.0.0.1:8000/docs`.

> Demo system. Always verify donor availability and medical eligibility through authorized channels.
