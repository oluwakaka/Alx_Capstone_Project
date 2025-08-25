# 🩺 Hypertension Medication Adherence Tracker API

## 📖 Introduction

Hypertension (high blood pressure) is a major risk factor for **stroke, heart attack, and kidney failure**.  
One of the biggest challenges in managing hypertension is **poor medication adherence** — patients forget doses, take them at the wrong times, or abandon treatment altogether.  

This project provides a **RESTful API** for tracking patient medication adherence, enabling:  
- Patients → to log and monitor their medication schedules.  
- Doctors → to review patient adherence history and intervene when necessary.  
- Admins → to manage users and system-wide operations.  

🔹 **Originality:** Unlike generic task trackers, this API is **healthcare-focused**, supporting structured medication schedules, adherence monitoring, and notifications — tailored to real-world chronic disease management.  

Built with:  
- [Django](https://www.djangoproject.com/)  
- [Django REST Framework](https://www.django-rest-framework.org/)  
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)  

---

## 📊 ERD — Entity Relationship Diagram

![ERD](docs/erd.png)

**Entity Overview**
- **User** → Base model with `username`, `email`, `password`, `role` (`patient`, `doctor`, `admin`)  
- **PatientProfile** → Extends User (date of birth, medical history)  
- **DoctorProfile** → Extends User (specialization)  
- **MedicationSchedule** → For patients; defines `medication_name`, `dosage`, `frequency`, `start_date`, `end_date`  
- **Activity** → Logs patient adherence (took/missed dose + timestamp)  
- **Notification** → Reminders/alerts linked to patients  

---

## 🔑 Authentication

The project uses **JWT (JSON Web Tokens)** for secure authentication.  

**Flow:**
1. Register → Create a new account  
2. Login → Get `access` + `refresh` tokens  
3. Use Token → Attach `Authorization: Bearer <ACCESS>` in headers  
4. Refresh → Use `refresh` token to get new `access`  
5. Logout → Blacklists refresh token  

---

## 📌 API Endpoints

### 🔐 Authentication
- `POST /api/auth/register/` → Register a new user  
- `POST /api/auth/login/` → Login (get tokens)  
- `GET /api/auth/profile/` → Get current user profile  
- `POST /api/auth/logout/` → Logout (blacklist refresh token)  

### 👤 Users
- `GET /api/users/` → List all users (admin only)  
- `GET /api/users/{id}/` → Get user details  

### 💊 Medication Schedules
- `GET /api/schedules/` → List all medication schedules  
- `POST /api/schedules/` → Create new schedule (patient/doctor)  
- `PUT /api/schedules/{id}/` → Update schedule  
- `DELETE /api/schedules/{id}/` → Delete schedule  

### 📋 Activities (Adherence Logs)
- `GET /api/activities/` → List activities  
- `POST /api/activities/` → Log medication intake/missed dose  

### 📈 Adherence
- `GET /api/patients/{patient_id}/adherence/summary/` → Get adherence summary  
- `GET /api/patients/{patient_id}/adherence/history/` → Get adherence history  

### 🔔 Notifications
- `GET /api/notifications/` → List notifications  
- `POST /api/notifications/send/` → Send new notification  

---

## 🧪 Example Requests

### Register
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
-H "Content-Type: application/json" \
-d '{"username": "alice", "email": "a@ex.com", "password": "StrongPass123!", "role": "patient", "date_of_birth": "1990-01-01"}'
