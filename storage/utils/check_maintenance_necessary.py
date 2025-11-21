from storage.models import Storage, Maintenance
from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

def check_maintenance_necessary():
    today = date.today()
    storage = Storage.objects.all()

    for s in storage:
        is_necessary = (s.upcoming_maintenance - today <= timedelta(days=30))
        
        if s.necessary_maintenance != is_necessary:
            s.necessary_maintenance = is_necessary
            s.save(update_fields=['necessary_maintenance'])
