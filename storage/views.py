from django.shortcuts import render
from django.views.generic.base import View
from .models import Maintenance, Storage
from django.db.models import OuterRef, Subquery
from datetime import date, timedelta


class Index(View):
    def get(self, request):
        latest_maintenance_subquery = (Maintenance.objects.filter(id=OuterRef('pk')).order_by('-maintenance_date').values('maintenance_date')[:1])
        latest_maintenance_providers = (Maintenance.objects.filter(id=OuterRef('pk')).order_by('-maintenance_date').values('maintenance_provider')[:1])
        upcoming_maintenance_subquery = (Maintenance.objects.filter(id=OuterRef('pk')).order_by('-maintenance_date').values('upcoming_maintenance')[:1])

        storages = Storage.objects.annotate(
            latest_maintenance_date=Subquery(latest_maintenance_subquery),
            latest_maintenance_suppliers=Subquery(latest_maintenance_providers),
            latest_maintenance_upcoming=Subquery(upcoming_maintenance_subquery)
        )

        for storage in storages:
            if storage.latest_maintenance_upcoming and storage.latest_maintenance_upcoming <= date.today() - timedelta(days=30):
                storage.necessary_maintenance = True
            else:
                storage.necessary_maintenance = False
            storage.save(update_fields=['necessary_maintenance'])

        requires = Storage.objects.filter(necessary_maintenance=True).count()
        not_requires = Storage.objects.filter(necessary_maintenance=False).count()

        return render(request, "storage/index.html", {
            "maintenances": storages,
            "requires": requires,
            "not_requires": not_requires
        })
    
class MachinaryDetail(View):
    def get(self, request, serial):
        machinary_detail = Storage.objects.get(serial=serial)
        maintenances_done = Maintenance.objects.filter(machinary_maintenance__serial=serial).order_by('-maintenance_date')
        return render(request, "storage/machinary_detail.html", {
            "maintenances": maintenances_done,
            "machinary": machinary_detail
        })