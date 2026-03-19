# Clinic API - Complete Project Guide (For Beginners)

This guide explains the **Clinic API** project in the simplest way possible. You can read this for interviews, code reviews, or learning.

---

## 🎯 What Does This Project Do?

Imagine a doctor's clinic that needs to manage:
- **Patients** (people who come to the doctor)
- **Appointments** (when they have doctor visits)

This project is a **web API** (a program that other programs can talk to) that helps manage:
1. Add new patients
2. Store patient information
3. Book appointments
4. Check appointment status
5. Get statistics (how many patients, how many appointments, etc.)

**Real example:**
- Someone calls the clinic and says "Add my patient record"
- The API receives this request and saves it to the database
- Then returns: "Patient added successfully"

---

## 🏗️ How Does It Work? (Simple Loop)

### Step 1: Request comes in
```
User → "Give me all patients" → API
```

### Step 2: API checks if user is logged in
```
API → "Do you have a valid token?" → User
```

### Step 3: If yes, API gets data from database
```
API → Database → Get all patients
```

### Step 4: API sends back response
```
API → "Here are all patients" → User
```

### Step 5: User gets the data
```
User receives: {
  "success": true,
  "data": [
    {"name": "rajesh kumar", "age": 35, ...},
    {"name": "priya sharma", "age": 28, ...}
  ]
}
```

---

## 📁 File Structure (What Each File Does)

### **Models** (`patients/models.py`)
Think of this as the **shape of data**.

```
Patient = {
  name: "rajesh kumar",
  age: 35,
  gender: "Male",
  contact_number: "9876543210",
  blood_group: "A+",
  created_at: "2025-03-19"
}

Appointment = {
  patient: Patient,
  doctor_name: "dr. sharma",
  appointment_date: "2025-03-25",
  reason: "regular checkup",
  status: "Pending"
}
```

**Simple analogy:** Models are like paper forms at a doctor's clinic. The form has blank fields (name, age, contact).

---

### **Serializers** (`patients/serializers.py`)
Think of this as the **translator between Python and JSON**.

**What it does:**
1. Takes Python data → converts to JSON (for sending to user)
2. Takes JSON from user → converts to Python (for saving to database)
3. Validates the data (checks if data is correct)

**Example:**
```
Python: Patient(name="rajesh", age=35)
     ↓ (Serializer)
JSON: {"name": "rajesh", "age": 35}
```

**Validation example:**
- Age must be 0-120 (check: if age > 120, reject)
- Phone number must be exactly 10 digits (check: if len != 10, reject)

---

### **Views** (`patients/views.py`)
Think of this as the **worker** who takes requests and sends responses.

**What it does:**
1. Receives request from user
2. Gets data from database
3. Processes data
4. Sends response back

**Example:**
```
User asks: GET /api/patients/
View does:
  1. Get all patients from database
  2. Convert to JSON format
  3. Return response with status "success"
```

**Who handles what:**
- `PatientViewSet` → handles patient requests (create, read, update, delete)
- `AppointmentViewSet` → handles appointment requests
- `StatsView` → handles statistics requests
- `LoginView` → handles login requests

---

### **Permissions** (`patients/permissions.py`)
Think of this as the **security guard** at the clinic.

**What it does:**
- Checks if user is logged in
- Checks what the user is allowed to do

**Rules:**
- **Staff users** (admin, doctor): Can do everything (create, read, update, delete)
- **Regular users** (patient): Can only read (view data, not change it)
- **Not logged in**: Cannot do anything

**Example:**
```
Regular user tries: POST /api/patients/ (create patient)
Security guard says: "No! You can only read, not write"
Regular user tries: GET /api/patients/ (view patients)
Security guard says: "Yes! Go ahead"
```

---

### **Admin** (`patients/admin.py`)
Think of this as the **dashboard** for managing data.

**What it does:**
- Shows patients and appointments in a user-friendly table
- Lets you search patients by name
- Lets you filter by gender, blood group, status
- Lets you add/edit/delete records manually

**Access:** `http://127.0.0.1:8000/admin/` with username/password

---

### **URLs** (`clinic_api/urls.py`)
Think of this as the **address list** of the API.

**What it does:**
Maps URLs to the right view.

**Example:**
```
GET /api/patients/        → PatientViewSet.list() (get all)
GET /api/patients/1/      → PatientViewSet.retrieve() (get one)
POST /api/patients/       → PatientViewSet.create() (add new)
PUT /api/patients/1/      → PatientViewSet.update() (change)
DELETE /api/patients/1/   → PatientViewSet.destroy() (delete)
```

---

### **Utils** (`clinic_api/utils.py`)
Think of this as the **response formatter**.

**What it does:**
- Makes sure all responses look the same
- Converts errors to JSON (not HTML)

**Example response:**
```json
{
  "success": true,
  "data": [...],
  "message": "Patients fetched successfully."
}
```

**Example error:**
```json
{
  "success": false,
  "data": {},
  "message": "Patient not found."
}
```

---

### **Settings** (`clinic_api/settings.py`)
Think of this as the **configuration file**.

**What it does:**
- Tells Django which apps to use
- Database settings
- Authentication settings
- API settings

**Important settings:**
```
INSTALLED_APPS = [
  'django.contrib.auth',        # User authentication
  'rest_framework',             # API framework
  'rest_framework.authtoken',   # Token authentication
  'patients',                   # Our app
]
```

---

## 🔐 Authentication (How Login Works)

### Step 1: User logs in
```
POST /api/auth/login/
{
  "username": "admin",
  "password": "admin123"
}
```

### Step 2: Server checks password
```
Database check: Is password correct?
Yes ✓
```

### Step 3: Server creates a token
```
Token = "auth-342410f7ee79f1579abaad597a175e3cd1e2ec38"
```

### Step 4: Server sends token back
```
Response: {
  "success": true,
  "data": {"token": "auth-342410f7ee79f1579abaad597a175e3cd1e2ec38"},
  "message": "Login successful."
}
```

### Step 5: User uses token for all requests
```
GET /api/patients/
Header: Authorization: Token auth-342410f7ee79f1579abaad597a175e3cd1e2ec38
```

**Analogy:** Token is like a **movie ticket**. You show it to get in, you don't need to buy it every time.

---

## � Complete File Documentation

### **Core Project Files**

#### `manage.py`
- Django command-line tool
- Run: `python manage.py runserver` for dev server
- Run: `python manage.py migrate` to apply database changes
- Run: `python manage.py createsuperuser` for admin account

#### `requirements.txt`
- Lists Python packages needed
- Install: `pip install -r requirements.txt`
- Contains: Django, DRF, etc.

#### `db.sqlite3`
- SQLite database file
- Stores all patient and appointment data
- Generated when Django runs

#### `setup.py`
- Python package setup

---

### **clinic_api/ (Main Django App Config)**

#### `settings.py`
- Django configuration file
- Database setup (SQLite)
- Apps: patients, rest_framework
- Authentication: Token based
- Disables DEBUG (returns JSON errors)
- REST Framework settings
- Custom exception handler

#### `urls.py`
- Maps all URLs to views
- Registers patient/appointment routes
- Registers stats and login endpoints
- Handles 404/500 errors
- Pattern: `router.register()`

#### `utils.py`
- `success_response()` - returns JSON success
- `error_response()` - returns JSON error
- `custom_exception_handler()` - converts all errors to JSON
- `handle_404()` - graceful 404 handler
- `handle_500()` - graceful 500 handler
- Ensures consistent response format

#### `wsgi.py`
- WSGI application entry point
- Used by production servers

---

### **patients/ (Main App)**

#### `models.py`
**Patient:**
- id (auto)
- name
- age (0-120)
- gender
- contact_number (10 digits)
- blood_group
- created_at

**Appointment:**
- id (auto)
- patient (ForeignKey)
- doctor_name
- appointment_date
- reason
- status (Pending/Confirmed/Cancelled)

#### `serializers.py`
**PatientSerializer:**
- Converts Patient → JSON
- Validates age (0-120)
- Validates phone (10 digits)
- Error messages

**AppointmentSerializer:**
- Converts Appointment → JSON
- Includes patient_name (read-only)

#### `views.py`
**PatientViewSet:**
- list() → GET /api/patients/
- retrieve() → GET /api/patients/{id}/
- create() → POST /api/patients/
- update() → PUT /api/patients/{id}/
- destroy() → DELETE /api/patients/{id}/
- Search: ?search=name

**AppointmentViewSet:**
- list() → GET /api/appointments/
- retrieve() → GET /api/appointments/{id}/
- create() → POST /api/appointments/
- update() → PUT /api/appointments/{id}/
- destroy() → DELETE /api/appointments/{id}/
- upcoming() → GET /api/appointments/upcoming/
- Filters: ?status=Pending, ?patient_id=1

**StatsView:**
- GET /api/stats/
- Total patients count
- Total appointments count
- Count by status

**LoginView:**
- POST /api/auth/login/
- Returns token

#### `permissions.py`
**IsStaffOrReadOnly:**
- Staff: full access (CRUD)
- Regular: read-only (GET)
- Not authenticated: denied

#### `admin.py`
**PatientAdmin:**
- Display: id, name, age, gender, blood_group, contact, created_at
- Search: name, contact, blood_group
- Filter: gender, blood_group

**AppointmentAdmin:**
- Display: id, patient, doctor, date, status
- Search: patient name, doctor, reason
- Filter: status, doctor

#### `migrations/`
- 0001_initial.py (creates Patient, Appointment tables)

---

### **Additional Files**

#### `add_sample_data.py`
- Adds 8 sample patients
- Creates appointments
- Run: `python add_sample_data.py`

#### `README.md`
- Quick start guide

#### `PROJECT_GUIDE.md` (This file)
- Complete documentation

---

### **File Quick Lookup**

| Task | File |
|------|------|
| Add patient field | `patients/models.py` |
| Add validation | `patients/serializers.py` |
| Change response format | `clinic_api/utils.py` |
| Add API endpoint | `patients/views.py` + `clinic_api/urls.py` |
| Restrict access | `patients/permissions.py` |
| Admin display | `patients/admin.py` |
| Configure Django | `clinic_api/settings.py` |
| Route URLs | `clinic_api/urls.py` |
| Add sample data | `add_sample_data.py` |

---

## �📊 Database (Where Data Lives)

### Patient Table
```
| id | name          | age | gender | contact_number | blood_group | created_at |
|----|---------------|-----|--------|----------------|-------------|------------|
| 1  | rajesh kumar  | 35  | Male   | 9876543210     | A+          | 2025-03-19 |
| 2  | priya sharma  | 28  | Female | 8765432109     | B+          | 2025-03-19 |
```

### Appointment Table
```
| id | patient_id | doctor_name  | appointment_date | reason           | status    |
|----|-----------|--------------|-----------------|------------------|-----------|
| 1  | 1         | dr. sharma   | 2025-03-25      | regular checkup  | Pending   |
| 2  | 2         | dr. malik    | 2025-03-26      | fever            | Confirmed |
```

**Relationship:** Each appointment has a `patient_id` that links to a patient. It's like saying "This appointment belongs to Patient #1".

---

## 🔄 How CRUD Works (Simple Operations)

### CREATE (Add new patient)
```
Input: {
  "name": "deepak sharma",
  "age": 38,
  "gender": "Male",
  "contact_number": "9111223344",
  "blood_group": "A+"
}

Process:
1. Check: Is phone 10 digits? ✓
2. Check: Is age 0-120? ✓
3. Save to database

Output: {
  "success": true,
  "data": {"id": 3, "name": "deepak sharma", ...},
  "message": "Patient created successfully."
}
```

### READ (Get patient)
```
GET /api/patients/1/

Process:
1. Find patient with id=1
2. Convert to JSON
3. Send back

Output: {
  "success": true,
  "data": {"id": 1, "name": "rajesh kumar", ...}
}
```

### UPDATE (Change patient)
```
PUT /api/patients/1/
Input: {"age": 36}

Process:
1. Find patient with id=1
2. Change age to 36
3. Save to database

Output: {
  "success": true,
  "data": {"id": 1, "age": 36, ...}
}
```

### DELETE (Remove patient)
```
DELETE /api/patients/1/

Process:
1. Find patient with id=1
2. Remove from database

Output: {
  "success": true,
  "message": "Patient deleted successfully."
}
```

---

## 🎓 Interview Questions & Answers

### Q1: What is an API?
**A:** API = "Application Programming Interface". It's a program that lets other programs talk to it. Like a menu at a restaurant - you ask for what you want, and the chef gives it to you.

### Q2: What is a token?
**A:** Token = a secret code that proves you are logged in. After login, you get a token. Then you show this token with every request to prove you're allowed to access data.

### Q3: What's the difference between POST, GET, PUT, DELETE?
**A:**
- **GET** = Read data (get patient list)
- **POST** = Add new data (create patient)
- **PUT** = Change data (update patient)
- **DELETE** = Remove data (delete patient)

### Q4: What is a serializer?
**A:** A converter. It changes Python objects to JSON (so we can send over internet) and JSON to Python (so we can save to database).

### Q5: What is a permission?
**A:** A rule that says who can do what. Like: "Staff can create/edit/delete, regular users can only read".

### Q6: What's authentication?
**A:** Checking if you are who you say you are. The API asks: "Are you really admin?" You prove it with your token.

### Q7: What is a model?
**A:** A model defines the shape of data. Like a template. "A Patient has: name, age, phone, blood type". Every patient follows this shape.

### Q8: Why do we show the same response format for all endpoints?
**A:** Consistency. The frontend (user interface) always knows what to expect:
```
{
  "success": true/false,
  "data": ...,
  "message": "..."
}
```

---

## 🧪 Basic Logic Examples

### Example 1: Search Patient by Name
```
User asks: GET /api/patients/?search=rajesh

Logic:
1. Get all patients: [pat1, pat2, pat3]
2. Filter where name contains "rajesh": [pat1]
3. Return: {
     "success": true,
     "data": [{"name": "rajesh kumar", ...}]
   }
```

### Example 2: Get Upcoming Appointments
```
User asks: GET /api/appointments/upcoming/

Logic:
1. Get current date/time: 2025-03-19 10:00 AM
2. Get appointments in next 7 days (3/19 to 3/26)
3. Sort by date (earliest first)
4. Return: {
     "success": true,
     "data": [
       {"appointment_date": "2025-03-20", ...},
       {"appointment_date": "2025-03-25", ...}
     ]
   }
```

### Example 3: Get Statistics
```
User asks: GET /api/stats/

Logic:
1. Count all patients: 8 patients
2. Count all appointments: 24 appointments
3. Count by status:
   - Pending: 8
   - Confirmed: 10
   - Cancelled: 6
4. Return: {
     "success": true,
     "data": {
       "total_patients": 8,
       "total_appointments": 24,
       "appointments_by_status": {
         "Pending": 8,
         "Confirmed": 10,
         "Cancelled": 6
       }
     }
   }
```

---

## 🚀 How to Run (Step by Step)

### Step 1: Go to project folder
```
cd C:\Users\sumit\OneDrive\Desktop\clinic_api
```

### Step 2: Activate virtual environment
```
venv\Scripts\activate
```

### Step 3: Start the server
```
python manage.py runserver
```

### Step 4: Open browser
```
http://127.0.0.1:8000/api/
```

---

## 🧪 How to Test

### Test 1: Login
```
POST http://127.0.0.1:8000/api/auth/login/
Header: Content-Type: application/json
Body: {"username": "admin", "password": "admin123"}

Expected: Token in response
```

### Test 2: Get all patients
```
GET http://127.0.0.1:8000/api/patients/
Header: Authorization: Token <your-token>

Expected: List of 8 patients
```

### Test 3: Create new patient
```
POST http://127.0.0.1:8000/api/patients/
Header: Authorization: Token <your-token>
Header: Content-Type: application/json
Body: {
  "name": "test user",
  "age": 25,
  "gender": "Male",
  "contact_number": "1234567890",
  "blood_group": "O+"
}

Expected: New patient created with id
```

### Test 4: Get stats
```
GET http://127.0.0.1:8000/api/stats/
Header: Authorization: Token <your-token>

Expected: Numbers (patients, appointments, status counts)
```

---

## 📝 Key Takeaways

1. **Models** = Data structure
2. **Serializers** = Converter between Python and JSON
3. **Views** = Logic (what to do with data)
4. **Permissions** = Access control (who can do what)
5. **URLs** = Routes (which URL goes to which view)
6. **Token Authentication** = Login system
7. **Same response format** = Consistency
8. **Validation** = Check data before saving

---

## 🎯 Interview Tip

When someone asks about this project, explain it like this:

> "This is a **clinic management API**. It stores patient information and appointments. 
> 
> When a user logs in, they get a **token** (like a ticket). Then they can:
> - **View** all patients and appointments
> - **Create** new patients and appointments (if they have permission)
> - **Update** existing records
> - **Delete** records
> - **Search** by name
> - **Get statistics**
>
> All responses follow the same format: success status, data, and message. This makes it easy for the frontend to understand what happened."

---

That's it! This project is a beginner-friendly REST API using Django and Django REST Framework. 🎉
