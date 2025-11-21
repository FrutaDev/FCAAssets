from django.shortcuts import render
from django.views.generic.base import View
from .models import Maintenance, Storage
from django.db.models import OuterRef, Subquery
from datetime import date, timedelta
from django.http import FileResponse, Http404
import os
from storage.forms import MaintenanceForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

class Index(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    def test_func(self):
        user = self.request.user
        return user.is_superuser or self.request.user.groups.filter(name='admins').exists()

    def get(self, request):
        latest_maintenance_subquery = (Maintenance.objects.filter(machinary_maintenance=OuterRef('pk'), is_approved=True).order_by('-maintenance_date').values('maintenance_date')[:1])
        latest_maintenance_providers = (Maintenance.objects.filter(machinary_maintenance=OuterRef('pk'), is_approved=True).order_by('-maintenance_date').values('maintenance_provider__name_provider')[:1])

        storages = Storage.objects.annotate(
            latest_maintenance_date=Subquery(latest_maintenance_subquery),
            latest_maintenance_suppliers=Subquery(latest_maintenance_providers),
        )

        requires = Storage.objects.filter(necessary_maintenance=True).count()
        not_requires = Storage.objects.filter(necessary_maintenance=False).count()



        return render(request, "storage/index.html", {
            "maintenances": storages,
            "requires": requires,
            "not_requires": not_requires
        })
    
class MachinaryDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def test_func(self):
        user = self.request.user
        return user.is_superuser or self.request.user.groups.filter(name='admins').exists()

    def get(self, request, serial):
        machinary_detail = Storage.objects.get(serial=serial)
        maintenances_done = Maintenance.objects.filter(machinary_maintenance__serial=serial).order_by('-maintenance_date')
        return render(request, "storage/machinary_detail.html", {
            "maintenances": maintenances_done,
            "machinary": machinary_detail
        })
    
class MaintenanceDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or self.request.user.groups.filter(name='admins').exists()

    def get(self, request, id):
        maintenance_detail = Maintenance.objects.get(id=id)
        return render(request, 'storage/maintenance_detail.html', {
            "maintenance_detail": maintenance_detail
        })
    
class MaintenanceFileDownload(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def test_func(self):
        user = self.request.user
        return user.is_superuser or self.request.user.groups.filter(name='admins').exists()
    
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

class CreateMaintenance(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = '/create-maintenance/'
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='proveedores').exists() or user.groups.filter(name='admins').exists()
    
    def get(self, request):
        form = MaintenanceForm()
        return render(request, 'storage/create_maintenance.html', {
            'form': form
        })
    
    def post(self, request):
        form = MaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'storage/create_maintenance.html', {
                'form': MaintenanceForm(),
                'success': True
            })
        return render(request, 'storage/create_maintenance.html', {
            'form': form
        })
    
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='proveedores').exists():
            return reverse_lazy('create-maintenance')
        return reverse_lazy('landing-page')