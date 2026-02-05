from storage.models import Storage, Maintenance
from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

def check_maintenance_necessary():
    today = date.today()
    storage = Storage.objects.all()
    to_update = []

    for s in storage:
        days_until = (s.upcoming_maintenance - today).days
        
        if days_until <= 0:
            new_status = "VE"
        elif days_until <= 30:
            new_status = "PV"
        else:
            new_status = "AD"  
        
        if s.necessary_maintenance != new_status:
            s.necessary_maintenance = new_status
            to_update.append(s)

    if to_update:
        Storage.objects.bulk_update(to_update, ['necessary_maintenance'])