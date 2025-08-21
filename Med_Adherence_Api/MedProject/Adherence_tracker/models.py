from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (("patient","Patient"),("doctor","Doctor"),("admin","Admin"))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="patient")

    def __str__(self):
        return f"{self.username} ({self.role})"

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    date_of_birth = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True, default="")

    def __str__(self):
        return f"Patient<{self.user.username}>"

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=120, blank=True, default="")
    # doctor ←→ patients assignment
    patients = models.ManyToManyField(PatientProfile, related_name="doctors", blank=True)

    def __str__(self):
        return f"Doctor<{self.user.username}>"

class MedicationSchedule(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="schedules")
    medication_name = models.CharField(max_length=120)
    dosage = models.CharField(max_length=60)
    frequency = models.CharField(max_length=60)  # e.g., "once daily"
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("end_date cannot be earlier than start_date")

    def __str__(self):
        return f"{self.medication_name} for {self.patient.user.username}"

class Activity(models.Model):
    STATUS_CHOICES = (("taken","Taken"),("missed","Missed"))
    schedule = models.ForeignKey(MedicationSchedule, on_delete=models.CASCADE, related_name="activities")
    date_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, default="")
    blood_pressure_reading = models.CharField(max_length=15, blank=True, default="")  # "120/80"

    class Meta:
        indexes = [models.Index(fields=["schedule","date_time"])]

    def __str__(self):
        return f"{self.schedule.medication_name} @ {self.date_time:%Y-%m-%d %H:%M} - {self.status}"

class Notification(models.Model):  # optional
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notif to {self.patient.user.username} @ {self.sent_at:%Y-%m-%d %H:%M}"
