from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, LoginView, LogoutView, MyProfileView, UserViewSet,
    MedicationScheduleViewSet, ActivityViewSet,
    AdherenceSummaryView, AdherenceHistoryView,
    NotificationViewSet, NotificationSendView
)

router = DefaultRouter()
router.register(r"auth/register", RegisterView, basename="register")
router.register(r"users", UserViewSet, basename="users")
router.register(r"schedules", MedicationScheduleViewSet, basename="schedules")
router.register(r"activities", ActivityViewSet, basename="activities")
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/profile/", MyProfileView.as_view(), name="profile"),
    path("patients/<int:patient_id>/adherence/summary/", AdherenceSummaryView.as_view(), name="adherence-summary"),
    path("patients/<int:patient_id>/adherence/history/", AdherenceHistoryView.as_view(), name="adherence-history"),
    path("notifications/send/", NotificationSendView.as_view(), name="notifications-send"),
]
