from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to the Med Adherence API 🚀</h1>")


urlpatterns = [
    path("admin/", admin.site.urls),

    # All API routes from your app
    path("api/", include("Adherence_tracker.urls")),
    path('', home),

    # Auth endpoints
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
