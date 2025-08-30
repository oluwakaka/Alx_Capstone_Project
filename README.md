🩺 Hypertension Medication Adherence API

📌 Project Overview

This is a Django REST Framework API that helps patients and healthcare providers track medication schedules and monitor adherence.

It solves the problem of patients forgetting or mismanaging their hypertension medications by allowing:

Patients to register and log in securely.

Patients/Doctors to create and view medication schedules.

Patients to log adherence activities (taken/missed).

⚡ Features

✅ User Authentication (JWT) – Secure registration & login.

✅ Medication Schedules – Create, view, and manage schedules.

✅ Adherence Logging – Track whether medication was taken or missed.

✅ Role-based Users – Patient & Doctor roles.

🛠️ Tech Stack

Backend: Django 5, Django REST Framework

Authentication: JWT (SimpleJWT)

Database: SQLite (default, can be switched to PostgreSQL/MySQL)

Tools: Postman (API testing)

🚀 Getting Started
1️⃣ Clone the Repo
git clone https://github.com/oluwakaka/Alx_Capstone_Project.git
cd Alx_Capstone_Project

2️⃣ Setup Virtual Environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Migrations
python manage.py migrate

5️⃣ Create Superuser (optional)
python manage.py createsuperuser

6️⃣ Start Development Server
python manage.py runserver


Server runs at: http://127.0.0.1:8000

📡 API Endpoints
🔑 Authentication
Register
POST /api/auth/register/


Request:

{
  "username": "cynthia",
  "email": "a@ct.com",
  "password": "StrongPass123!",
  "role": "patient",
  "date_of_birth": "1990-01-01"
}


Response:

{
  "message": "User registered successfully.",
  "user": {
    "id": 1,
    "username": "cynthia",
    "email": "a@ct.com",
    "role": "patient"
  }
}

Login
POST /api/auth/login/


Request:

{
  "username": "cynthia",
  "password": "StrongPass123!"
}


Response:

{
  "message": "Login successful.",
  "refresh": "xxxxx",
  "access": "xxxxx"
}

📅 Schedules
Get All Schedules
GET /api/schedules/
Authorization: Bearer <ACCESS_TOKEN>


Response:

[
  {
    "id": 1,
    "patient": 1,
    "medication_name": "Amlodipine",
    "dosage": "10mg",
    "frequency": "daily",
    "start_date": "2025-08-26",
    "end_date": "2025-09-26"
  }
]

Create Schedule
POST /api/schedules/
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json


Request:

{
  "patient": 1,
  "medication_name": "Amlodipine",
  "dosage": "10mg",
  "frequency": "daily",
  "start_date": "2025-08-26",
  "end_date": "2025-09-26"
}


Response:

{
  "message": "Schedule created successfully.",
  "data": {
    "id": 1,
    "patient": 1,
    "medication_name": "Amlodipine",
    "dosage": "10mg",
    "frequency": "daily",
    "start_date": "2025-08-26",
    "end_date": "2025-09-26"
  }
}

💊 Adherence Activities
Log Activity
POST /api/activities/
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json


Request:

{
  "schedule": 1,
  "status": "taken",
  "date_time": "2025-08-27T10:00:00Z"
}


Response:

{
  "message": "Activity logged successfully.",
  "data": {
    "id": 1,
    "schedule": 1,
    "status": "taken",
    "date_time": "2025-08-27T10:00:00Z"
  }
}

📽️ Demo Video

👉 Watch my Loom demo here: [https://www.loom.com/share/1d4a7bc3521a47bbbebac87466e46728?sid=17755d74-0dbc-41e2-801f-ce08f53ff9ed]

👨‍💻 Author

Name: Kaka Olalekan Okikiola

GitHub: oluwakaka

LinkedIn: Kaka Olalekan
