from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, PatientProfile, DoctorProfile, MedicationSchedule, Activity, Notification

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (("Role", {"fields": ("role",)}),)

admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(MedicationSchedule)
admin.site.register(Activity)
admin.site.register(Notification)
