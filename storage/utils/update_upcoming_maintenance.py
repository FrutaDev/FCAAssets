from storage.models import Maintenance, Storage
from datetime import timedelta
from django.db.models import OuterRef, Subquery


def update_upcoming_maintenance():

    latest_maintenance = Maintenance.objects.filter(
        machinary_maintenance=OuterRef('pk'), is_approved=True
    ).order_by('-maintenance_date')

    storage = Storage.objects.annotate(
    last_maintenance_date=Subquery(latest_maintenance.values('maintenance_date')[:1]),
    last_maintenance_id=Subquery(latest_maintenance.values('id')[:1])
)
    for s in storage:
        if s.last_maintenance_date is None:
            continue
        new_upcoming = s.last_maintenance_date + timedelta(days=365)
        if s.upcoming_maintenance != new_upcoming:
            s.upcoming_maintenance = new_upcoming
            s.save(update_fields=['upcoming_maintenance'])
        