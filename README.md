# Healthcare Backend (Django + DRF + PostgreSQL)

A REST API implementation for the Django healthcare assignment. It includes JWT authentication, patient and doctor management, patient–doctor mappings, input validation, environment-based configuration, and ownership checks for patient data.

## Requirements

- Python 3.10+
- PostgreSQL 14+
- pip

## Setup (Windows PowerShell)

### 1. Clone the repository

```powershell
git clone https://github.com/aman07052005/Healthcare-Backend-Django_WhatBytes.git
cd Healthcare-Backend-Django_WhatBytes
```

### 2. Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create your local environment file:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and configure `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and your PostgreSQL credentials. Use a strong, randomly generated secret key and never commit your `.env` file.

### 5. Create the PostgreSQL database

Ensure PostgreSQL is running, then create the database using your PostgreSQL client:

```sql
CREATE DATABASE healthcare_db;
```

Make sure the database name and credentials match the values in `.env`.

### 6. Apply migrations

```powershell
python manage.py migrate
```

### 7. Create an administrator account (optional)

```powershell
python manage.py createsuperuser
```

### 8. Start the development server

```powershell
python manage.py runserver
```

The API will be available at:

`http://127.0.0.1:8000`

## Authentication

Authentication uses JSON Web Tokens (JWT) through Django REST Framework SimpleJWT.

### Register

**POST** `/api/auth/register/`

Request body:

```json
{
  "name": "Aman Yadav",
  "email": "aman@example.com",
  "password": "Use-A-Strong-Password-123!"
}
```

Register a user account. The password must satisfy the application's password validation rules.

### Login

**POST** `/api/auth/login/`

Request body:

```json
{
  "email": "aman@example.com",
  "password": "Use-A-Strong-Password-123!"
}
```

The response includes `access` and `refresh` JWTs.

For protected endpoints, include the access token in the request header:

```http
Authorization: Bearer <access-token>
```

### Refresh access token

**POST** `/api/auth/token/refresh/`

Request body:

```json
{
  "refresh": "<refresh-token>"
}
```

Use the refresh token to obtain a new access token.

## API Endpoints

### Authentication

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register/` | Register a user |
| POST | `/api/auth/login/` | Obtain JWT tokens |
| POST | `/api/auth/token/refresh/` | Refresh an access token |

### Patients

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/patients/` | Create a patient owned by the authenticated user |
| GET | `/api/patients/` | List the authenticated user's patients |
| GET | `/api/patients/{id}/` | Retrieve one of the user's patients |
| PUT | `/api/patients/{id}/` | Fully update an owned patient |
| PATCH | `/api/patients/{id}/` | Partially update an owned patient |
| DELETE | `/api/patients/{id}/` | Delete an owned patient |

### Doctors

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/` | List doctors |
| GET | `/api/doctors/{id}/` | Retrieve a doctor |
| PUT | `/api/doctors/{id}/` | Fully update a doctor |
| PATCH | `/api/doctors/{id}/` | Partially update a doctor |
| DELETE | `/api/doctors/{id}/` | Delete a doctor |

### Patient–Doctor Mappings

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to an owned patient |
| GET | `/api/mappings/` | List mappings for the authenticated user's patients |
| GET | `/api/mappings/{patient_id}/` | List doctors assigned to a specific patient |
| DELETE | `/api/mappings/{mapping_id}/` | Remove a patient–doctor mapping |

All patient, doctor, and mapping endpoints require JWT authentication.

Users can access and manage only their own patient records and associated mappings. Doctor records are shared among authenticated users. Duplicate doctor assignments to the same patient are rejected.

## Example Request Payloads

### Create a patient

**POST** `/api/patients/`

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

### Create a doctor

**POST** `/api/doctors/`

```json
{
  "name": "Dr. Mehta",
  "specialization": "Cardiology",
  "email": "doctor@example.com",
  "phone": "9876501234",
  "clinic_address": "New Delhi"
}
```

### Assign a doctor to a patient

**POST** `/api/mappings/`

```json
{
  "patient": 1,
  "doctor": 1
}
```

The patient ID must belong to the authenticated user. The doctor ID must identify an existing doctor.

## Notes and Implementation Details

- **Patient–Doctor Mapping Routes:** `GET /api/mappings/<patient_id>/` retrieves the doctors assigned to a specific patient. The mapping routes are explicitly configured in `mappings/urls.py`. For `DELETE /api/mappings/<mapping_id>/`, the path ID identifies the mapping to be removed, as required by the assignment.
- **Update Operations:** `PUT` supports full resource updates, while `PATCH` supports partial updates for patient and doctor records.
- **Input Validation:** Patient age is validated, user registration applies password validation, and duplicate patient–doctor assignments are prevented.
- **Security Configuration:** Sensitive configuration is read from environment variables. Before production deployment, set `DEBUG=False`, use a strong secret key, restrict `ALLOWED_HOSTS`, and configure HTTPS and other appropriate security settings.
- **Database Configuration:** PostgreSQL must be running and correctly configured before applying migrations or starting the application.
- **API Testing:** Verify endpoints using Postman, `curl`, or another API client, including authentication, validation, and access-control behavior.

## Running Tests

Run the project's Django tests with:

```powershell
python manage.py test
```

You can also check the Django configuration with:

```powershell
python manage.py check
```

## Technology Stack

- **Backend:** Python, Django, Django REST Framework
- **Authentication:** JWT using Django REST Framework SimpleJWT
- **Database:** PostgreSQL
- **ORM:** Django ORM
- **Configuration:** Environment variables using `django-environ`

