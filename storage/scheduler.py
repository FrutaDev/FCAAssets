
from storage.utils.email import job_send_maintenance_emails
from storage.utils.check_maintenance_necessary import check_maintenance_necessary
from storage.utils.update_upcoming_maintenance import update_upcoming_maintenance


def jobs_scheduler():
    job_send_maintenance_emails()
    update_upcoming_maintenance()
    check_maintenance_necessary()
    

import os 
import tempfile
import sys
from apscheduler.schedulers.background import BackgroundScheduler


LOCK_FILE = os.path.join(tempfile.gettempdir(), "scheduler.lock")

def start_scheduler():
    if "runserver" in sys.argv and os.environ.get("RUN_MAIN") != "true":
        return
    
    # Evitar 
    if os.path.exists(LOCK_FILE):
        print("Scheduler ya está corriendo")
        return

    open(LOCK_FILE, "w").close()
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        jobs_scheduler,
        trigger="cron",
        hour=7,
        minute=0,
    )
    scheduler.start()
