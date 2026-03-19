# Clinic API - Django REST Framework 

This is  Django REST API project that manages **patients** and **appointments**.
It uses **Token authentication**, and all API routes require a logged-in user or a normal.

---
---

## Setup 
From the project root (`clinic_api/`):
1) Create and activate the virtual environment (Windows example):
```powershell
python -m venv venv
venv\Scripts\activate
```
2) Install dependencies:
```powershell
pip install -r requirements.txt
```
3) Run the setup script (creates database, users, sample data):
```powershell
python setup.py
```
4) Start the server:
```powershell
python manage.py runserver
```
> If you get "manage.py not found", you are probably in `clinic_api/clinic_api/`.
> Go back to `clinic_api/` and run commands there.



## How to check it is working

### 1) Get a token 

POST `/api/auth/login/` with:

```json
{ "username": "admin", "password": "admin123" }
```

If the credentials are wrong, you will get an error like:

```json
{ "success": false, "message": "Invalid credentials. Please check username and password." }
```

### 2) Use the token for API calls

Add header:

```
Authorization: Token <token_here>
```

Then try:

- `GET /api/patients/` should return a list of patients.
- `GET /api/appointments/` should return appointments.

If you get `401 Unauthorized`, check that the token header is correct.

---

## Main API endpoints (quick list)

- `POST /api/auth/login/` — get token
- `GET /api/patients/` — list patients
- `GET /api/patients/<id>/` — patient details
- `POST /api/patients/` — create patient 
- `GET /api/appointments/` — list appointments
- `GET /api/stats/` — statistics

---

## Permissions (who can do what)

- **Staff users** (like `admin`): can create, update, delete, and read.
- **Regular users** (like `user1`): can only read .
- **Unauthenticated**: not allowed (401 error).
---

## Response structure 

Success example:
```json
{
  "success": true,
  "data": { ... },
  "message": "..."
}
```


---

## Admin panel

Visit `http://127.0.0.1:8000/admin/` with:

- Username: `admin`
- Password: `admin123`

You can add/edit patients and appointments there.
