from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView, MyProfileView, UserViewSet,
    MedicationScheduleViewSet, ActivityViewSet,
    AdherenceSummaryView, AdherenceHistoryView,
    NotificationViewSet, NotificationSendView
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"schedules", MedicationScheduleViewSet, basename="schedules")
router.register(r"activities", ActivityViewSet, basename="activities")
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    # Router endpoints
    path("", include(router.urls)),

    # Auth (your custom ones)
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/profile/", MyProfileView.as_view(), name="profile"),

    # JWT tokens
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Adherence endpoints
    path("patients/<int:patient_id>/adherence/summary/", AdherenceSummaryView.as_view(), name="adherence-summary"),
    path("patients/<int:patient_id>/adherence/history/", AdherenceHistoryView.as_view(), name="adherence-history"),

    # Notifications
    path("notifications/send/", NotificationSendView.as_view(), name="notifications-send"),
]
