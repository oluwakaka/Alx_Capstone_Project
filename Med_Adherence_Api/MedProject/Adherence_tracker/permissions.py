from rest_framework.permissions import BasePermission
from .models import PatientProfile, DoctorProfile, MedicationSchedule, Activity

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

class IsOwnerPatientOrAssignedDoctor(BasePermission):
    """
    Patients: access own resources.
    Doctors: access resources of assigned patients (read; write policy in views).
    Admin: full access.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # resolve obj -> PatientProfile
        if isinstance(obj, MedicationSchedule):
            patient = obj.patient
        elif isinstance(obj, Activity):
            patient = obj.schedule.patient
        else:
            return request.user.role == "admin"

        if request.user.role == "admin":
            return True
        if request.user.role == "patient":
            return patient.user_id == request.user.id
        if request.user.role == "doctor":
            try:
                return request.user.doctor_profile.patients.filter(pk=patient.pk).exists()
            except DoctorProfile.DoesNotExist:
                return False
        return False
