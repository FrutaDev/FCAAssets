from django.shortcuts import render
from django.views.generic.base import View
from .models import Maintenance, Storage
from django.db.models import OuterRef, Subquery
from datetime import date, timedelta
from django.http import FileResponse, Http404
import os


class Index(View):
    def get(self, request):
        latest_maintenance_subquery = (Maintenance.objects.filter(id=OuterRef('pk')).order_by('-maintenance_date').values('maintenance_date')[:1])
        latest_maintenance_providers = (Maintenance.objects.filter(id=OuterRef('pk')).order_by('-maintenance_date').values('maintenance_provider__name_provider')[:1])
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
    
class MaintenanceDetail(View):
    def get(self, request, id):
        maintenance_detail = Maintenance.objects.get(id=id)
        return render(request, 'storage/maintenance_detail.html', {
            "maintenance_detail": maintenance_detail
        })
    
class MaintenanceFileDownload(View):
    def get(self, request, id):
        try:
            maintenance = Maintenance.objects.get(id=id)
            if not maintenance:
                raise Http404("Este mantenimiento no tiene archivo asociado.")
            file_path = maintenance.maintenance_file.path
            if not file_path:
                raise Http404("El archivo no se encuentra en el servidor.")
            file_name = os.path.basename(file_path)
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
            return response
        except:
            raise Http404("El archivo de mantenimiento no existe.")