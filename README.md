# Blood Donation Platform

A privacy-conscious donor discovery and emergency blood-request platform with blood-group and city matching.

## Features
- Donor registration and availability
- Blood-group and city filtering
- Emergency request workflow
- Operations dashboard-ready API
- Browser donor search at `/`
- Swagger/OpenAPI at `/docs`
- Automated API tests
- Docker-ready deployment

## Stack
Python · FastAPI · Pydantic · Docker

## Run locally
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload
```
Open `http://127.0.0.1:8000/`.

## Core API
`POST /donors`, `GET /donors`, `POST /requests`, `GET /requests`, and `GET /dashboard`.

> Demo system. Verify donor availability, eligibility, identity, and medical suitability through authorized healthcare channels. Avoid exposing donor contact information publicly.
