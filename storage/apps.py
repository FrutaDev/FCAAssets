from django.apps import AppConfig
import os
import tempfile


class StorageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'storage'


    def ready(self):
        from storage.scheduler import start_scheduler
        start_scheduler()
        