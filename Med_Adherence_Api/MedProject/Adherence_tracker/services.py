from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q
from .models import Activity, PatientProfile

def adherence_summary_for_patient(patient: PatientProfile, days: int = 7):
    start = timezone.now() - timedelta(days=days)
    qs = Activity.objects.filter(schedule__patient=patient, date_time__gte=start)
    agg = qs.aggregate(total=Count("id"), taken=Count("id", filter=Q(status="taken")))
    total = agg["total"] or 0
    taken = agg["taken"] or 0
    rate = round((taken / total) * 100, 2) if total else 0.0
    return {"total": total, "taken": taken, "rate": rate}
