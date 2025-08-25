from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .models import (
    User, PatientProfile, DoctorProfile,
    MedicationSchedule, Activity, Notification
)
from .serializers import (
    RegisterSerializer, UserSerializer,
    MedicationScheduleSerializer, ActivitySerializer, NotificationSerializer
)
from .permissions import IsAdmin, IsOwnerPatientOrAssignedDoctor
from .services import adherence_summary_for_patient

# ---------- AUTH ----------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class LogoutView(APIView):
    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"detail": "refresh token required"}, status=400)
        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "invalid token"}, status=400)


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        user = request.user
        user.email = request.data.get("email", user.email)
        user.save()

        if user.role == "patient" and hasattr(user, "patient_profile"):
            from .serializers import PatientProfileSerializer
            ser = PatientProfileSerializer(
                user.patient_profile, data=request.data, partial=True
            )
            ser.is_valid(raise_exception=True)
            ser.save()

        if user.role == "doctor" and hasattr(user, "doctor_profile"):
            from .serializers import DoctorProfileSerializer
            ser = DoctorProfileSerializer(
                user.doctor_profile, data=request.data, partial=True
            )
            ser.is_valid(raise_exception=True)
            ser.save()

        return Response(UserSerializer(user).data)


# ---------- USER MANAGEMENT (Doctor/Admin only) ----------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related("patient_profile", "doctor_profile")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]


# ---------- SCHEDULES ----------
class MedicationScheduleViewSet(viewsets.ModelViewSet):
    queryset = MedicationSchedule.objects.select_related("patient", "patient__user")
    serializer_class = MedicationScheduleSerializer
    permission_classes = [IsAuthenticated, IsOwnerPatientOrAssignedDoctor]

    def get_queryset(self):
        user = self.request.user
        base = MedicationSchedule.objects.select_related("patient", "patient__user")
        if user.role == "admin":
            return base
        if user.role == "patient":
            return base.filter(patient__user=user)
        if user.role == "doctor":
            try:
                doc = user.doctor_profile
                return base.filter(patient__in=doc.patients.all())
            except DoctorProfile.DoesNotExist:
                return base.none()
        return base.none()

    def perform_create(self, serializer):
        user = self.request.user
        patient = serializer.validated_data["patient"]
        if user.role == "patient" and patient.user_id != user.id:
            raise PermissionError("patients can only create for themselves")
        if user.role == "doctor":
            doc = user.doctor_profile
            if not doc.patients.filter(pk=patient.pk).exists():
                raise PermissionError("doctor not assigned to this patient")
        serializer.save()


# ---------- ACTIVITIES ----------
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.select_related("schedule", "schedule__patient", "schedule__patient__user")
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated, IsOwnerPatientOrAssignedDoctor]

    def get_queryset(self):
        user = self.request.user
        base = Activity.objects.select_related("schedule", "schedule__patient", "schedule__patient__user")
        if user.role == "admin":
            return base
        if user.role == "patient":
            return base.filter(schedule__patient__user=user)
        if user.role == "doctor":
            try:
                doc = user.doctor_profile
                return base.filter(schedule__patient__in=doc.patients.all())
            except DoctorProfile.DoesNotExist:
                return base.none()
        return base.none()

    def update(self, request, *args, **kwargs):
        if request.user.role == "doctor":
            return Response({"detail": "doctors cannot modify activities"}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role == "doctor":
            return Response({"detail": "doctors cannot delete activities"}, status=403)
        return super().destroy(request, *args, **kwargs)


# ---------- ANALYTICS ----------
class AdherenceSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        try:
            patient = PatientProfile.objects.select_related("user").get(pk=patient_id)
        except PatientProfile.DoesNotExist:
            return Response({"detail": "patient not found"}, status=404)

        u = request.user
        allowed = (
            u.role == "admin"
            or (u.role == "patient" and patient.user_id == u.id)
            or (u.role == "doctor" and u.doctor_profile.patients.filter(pk=patient.pk).exists())
        )
        if not allowed:
            return Response({"detail": "forbidden"}, status=403)

        rng = request.query_params.get("range", "7d")
        days = 7 if rng == "7d" else 30
        data = adherence_summary_for_patient(patient, days=days)
        return Response({
            "patient_id": patient_id,
            "range": rng,
            "total_doses": data["total"],
            "taken_doses": data["taken"],
            "adherence_rate": f"{data['rate']:.2f}%"
        })


class AdherenceHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        try:
            patient = PatientProfile.objects.select_related("user").get(pk=patient_id)
        except PatientProfile.DoesNotExist:
            return Response({"detail": "patient not found"}, status=404)

        u = request.user
        allowed = (
            u.role == "admin"
            or (u.role == "patient" and patient.user_id == u.id)
            or (u.role == "doctor" and u.doctor_profile.patients.filter(pk=patient.pk).exists())
        )
        if not allowed:
            return Response({"detail": "forbidden"}, status=403)

        qs = Activity.objects.filter(schedule__patient=patient).order_by("-date_time")
        if start:
            qs = qs.filter(date_time__date__gte=start)
        if end:
            qs = qs.filter(date_time__date__lte=end)
        return Response({"patient_id": patient_id, "results": ActivitySerializer(qs, many=True).data})


# ---------- NOTIFICATIONS ----------
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related("patient", "patient__user")
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]


class NotificationSendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        patient_id = request.data.get("patient")
        msg = request.data.get("message")
        if not (patient_id and msg):
            return Response({"detail": "patient and message required"}, status=400)

        try:
            patient = PatientProfile.objects.get(pk=patient_id)
        except PatientProfile.DoesNotExist:
            return Response({"detail": "patient not found"}, status=404)

        Notification.objects.create(patient=patient, message=msg, sent_at=timezone.now())
        return Response({"detail": "notification queued"}, status=201)
