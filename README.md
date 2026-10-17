# Healthcare Backend (Django + DRF + PostgreSQL)

A REST API implementation for the supplied Django healthcare assignment. It includes JWT authentication, patient and doctor management, patient-doctor mappings, validation, environment-based configuration, and ownership checks for patient data.

## Requirements
- Python 3.10+
- PostgreSQL 14+
- pip

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `SECRET_KEY` and your PostgreSQL credentials. Create the database in PostgreSQL:

```sql
CREATE DATABASE healthcare_db;
```

Then run:

```powershell
python manage.py makemigrations accounts patients doctors mappings
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API base URL: `http://127.0.0.1:8000`

## Authentication

### Register
`POST /api/auth/register/`

```json
{
  "name": "Aman Yadav",
  "email": "aman@example.com",
  "password": "Use-A-Strong-Password-123!"
}
```

### Login
`POST /api/auth/login/`

```json
{
  "email": "aman@example.com",
  "password": "Use-A-Strong-Password-123!"
}
```

Response includes `access` and `refresh` JWTs. For protected endpoints, add this header:

`Authorization: Bearer <access-token>`

### Refresh
`POST /api/auth/token/refresh/`

```json
{"refresh": "<refresh-token>"}
```

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register/` | Register a user |
| POST | `/api/auth/login/` | Obtain JWT tokens |
| POST | `/api/auth/token/refresh/` | Refresh an access token |
| POST | `/api/patients/` | Create a patient owned by current user |
| GET | `/api/patients/` | List current user's patients |
| GET | `/api/patients/{id}/` | Retrieve one of current user's patients |
| PUT/PATCH | `/api/patients/{id}/` | Update own patient |
| DELETE | `/api/patients/{id}/` | Delete own patient |
| POST | `/api/doctors/` | Create doctor |
| GET | `/api/doctors/` | List doctors |
| GET | `/api/doctors/{id}/` | Retrieve doctor |
| PUT/PATCH | `/api/doctors/{id}/` | Update doctor |
| DELETE | `/api/doctors/{id}/` | Delete doctor |
| POST | `/api/mappings/` | Assign doctor to own patient |
| GET | `/api/mappings/` | List mappings for own patients |
| GET | `/api/mappings/{patient_id}/` | List doctors assigned to a patient |
| DELETE | `/api/mappings/{mapping_id}/` | Remove mapping |

All patient, doctor and mapping endpoints require JWT authentication. A user only sees and changes their own patients and mappings. Doctor records are shared across authenticated users as requested by the assignment. Duplicate doctor assignments to a patient are rejected.

## Example payloads

Patient (`POST /api/patients/`):
```json
{
  "name": "Riya Sharma",
  "age": 29,
  "gender": "Female",
  "email": "riya@example.com",
  "phone": "9876543210",
  "address": "Delhi",
  "medical_history": "No known allergies"
}
```

Doctor (`POST /api/doctors/`):
```json
{
  "name": "Dr. Mehta",
  "specialization": "Cardiology",
  "email": "doctor@example.com",
  "phone": "9876501234",
  "clinic_address": "New Delhi"
}
```

Mapping (`POST /api/mappings/`):
```json
{
  "patient": 1,
  "doctor": 1
}
```

## Notes and Implementation Details

- **Patient–Doctor Mapping Routes:** The endpoint `GET /api/mappings/<patient_id>/` retrieves doctors assigned to a specific patient. It is configured before the router-generated mapping detail routes to avoid URL conflicts and ensure the intended endpoint is matched.
- **Update Operations:** `PUT` supports full resource updates, while `PATCH` supports partial updates for patient and doctor records.
- **Security Configuration:** Environment variables are used for sensitive configuration. Before production deployment, set `DEBUG=False`, configure a strong secret key, restrict `ALLOWED_HOSTS`, and enable HTTPS and appropriate security settings.
- **Database and Testing:** PostgreSQL must be running and correctly configured before applying migrations or starting the application. After setup, verify the API endpoints using Postman or `curl`, including authentication, validation, and access-control behavior.
