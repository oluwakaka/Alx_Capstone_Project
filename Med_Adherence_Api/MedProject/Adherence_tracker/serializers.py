from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import (
    User, PatientProfile, DoctorProfile,
    MedicationSchedule, Activity, Notification
)

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ["id","date_of_birth","medical_history"]

class DoctorProfileSerializer(serializers.ModelSerializer):
    patients = serializers.PrimaryKeyRelatedField(queryset=PatientProfile.objects.all(), many=True, required=False)
    class Meta:
        model = DoctorProfile
        fields = ["id","specialization","patients"]

class UserSerializer(serializers.ModelSerializer):
    patient_profile = PatientProfileSerializer(read_only=True)
    doctor_profile = DoctorProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ["id","username","email","role","patient_profile","doctor_profile"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    date_of_birth = serializers.DateField(write_only=True, required=False)
    medical_history = serializers.CharField(write_only=True, required=False, allow_blank=True)
    specialization = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["username","email","password","role","date_of_birth","medical_history","specialization"]

    def create(self, validated):
        role = validated.get("role","patient")
        user = User(username=validated["username"], email=validated.get("email",""), role=role)
        user.set_password(validated["password"])
        user.save()
        if role == "patient":
            PatientProfile.objects.create(
                user=user,
                date_of_birth=validated.get("date_of_birth"),
                medical_history=validated.get("medical_history",""),
            )
        elif role == "doctor":
            DoctorProfile.objects.create(
                user=user,
                specialization=validated.get("specialization","")
            )
        return user

class MedicationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationSchedule
        fields = "__all__"

    def validate(self, attrs):
        if attrs["end_date"] < attrs["start_date"]:
            raise serializers.ValidationError({"end_date":"cannot be earlier than start_date"})
        return attrs

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
