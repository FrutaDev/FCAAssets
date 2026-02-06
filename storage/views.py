from django.shortcuts import render
from django.views.generic.base import View
from .models import Maintenance, Storage, Labs, Types
from django.db.models import OuterRef, Subquery
from datetime import date, timedelta
from django.http import FileResponse, Http404
import os
from storage.forms import MaintenanceForm, StorageForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, FileResponse, Http404
import json
from .models import Maintenance, Storage, Labs, Types, Brand
from django.db.models import Q
from django.core.paginator import Paginator

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

        if request.GET.get('q'):
            query = request.GET.get('q')
            storages = storages.filter(
                Q(serial__icontains=query) | 
                Q(name__type_name__icontains=query) | 
                Q(brand__brand_name__icontains=query) | 
                Q(lab_name__lab_name__icontains=query)
            )

        paginator = Paginator(storages, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        up_to_date = Storage.objects.filter(necessary_maintenance='AD').count()
        expiring = Storage.objects.filter(necessary_maintenance='PV').count()
        expired = Storage.objects.filter(necessary_maintenance='VE').count()
        for storage in storages:
            print("storage", storage.necessary_maintenance)

        return render(request, "storage/index.html", {
            "maintenances": page_obj,
            "page_obj": page_obj,
            "up_to_date": up_to_date,
            "expiring": expiring,
            "expired": expired,
            "expiring": expiring,
            "expired": expired,
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
        
        paginator = Paginator(maintenances_done, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "storage/machinary_detail.html", {
            "maintenances": page_obj,
            "page_obj": page_obj,
            "machinary": machinary_detail,
        })
    
class MaintenanceDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or self.request.user.groups.filter(name='admins').exists()

    def get(self, request, id):
        maintenance_detail = Maintenance.objects.get(id=id)
        print("maintenance_detail", maintenance_detail)
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
    
class CreateMachinary(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = '/create-machinary/'

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='admins').exists()
    
    def get(self, request):
        form = StorageForm()
        return render(request, 'storage/create-machinary.html', {
            'form': form
        })
    
    def post(self, request):
        form = StorageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'storage/create-machinary.html', {
                'form': StorageForm(),
                'success': True
            })
        return render(request, 'storage/create-machinary.html', {
            'form': form
        })
    
class EditMachinary(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = '/edit-machinary/'

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='admins').exists()
    
    def get(self, request, serial):
        machinary = Storage.objects.get(serial=serial)
        form = StorageForm(instance=machinary)
        return render(request, 'storage/edit-machinary.html', {
            'form': form,
            'machinary': machinary
        })
    
    def post(self, request, serial):
        machinary = Storage.objects.get(serial=serial)
        form = StorageForm(request.POST, request.FILES, instance=machinary)
        if form.is_valid():
            form.save()
            return render(request, 'storage/edit-machinary.html', {
                'form': form,
                'machinary': machinary,
                'success': True
            })
        return render(request, 'storage/edit-machinary.html', {
            'form': form,
            'machinary': machinary
        })
    
        return render(request, 'storage/edit-machinary.html', {
            'form': form,
            'machinary': machinary
        })
    
class CreateLab(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='admins').exists()

    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if name:
                lab = Labs.objects.create(lab_name=name)
                return JsonResponse({'id': lab.id, 'name': lab.lab_name, 'success': True}) # type: ignore
            return JsonResponse({'success': False, 'error': 'Nombre es requerido'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

class CreateBrand(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='admins').exists()

    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if name:
                brand = Brand.objects.create(brand_name=name) # type: ignore
                return JsonResponse({'id': brand.id, 'name': brand.brand_name, 'success': True}) # type: ignore
            return JsonResponse({'success': False, 'error': 'Nombre es requerido'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

class CreateType(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='admins').exists()

    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if name:
                type_obj = Types.objects.create(type_name=name)
                return JsonResponse({'id': type_obj.id, 'name': type_obj.type_name, 'success': True}) # type: ignore
            return JsonResponse({'success': False, 'error': 'Nombre es requerido'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='proveedores').exists():
            return reverse_lazy('create-maintenance')
        return reverse_lazy('landing-page')

class Search(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def test_func(self):
        user = self.request.user
        return user.is_superuser or self.request.user.groups.filter(name='admins').exists()
    
    def get(self, request):
        laboratory = request.GET.get('laboratorio')
        machinary_type = request.GET.get('maquinaria')
        machinary = None
        if machinary_type:
            machinary = Types.objects.get(id=machinary_type)
        if machinary_type:
            results = Storage.objects.filter(lab_name=laboratory, name=machinary_type)
            # .values('serial', 'name__type_name', 'brand__brand_name', 'lab_name', 'image', 'upcoming_maintenance', 'necessary_maintenance')
        else:
            results = Storage.objects.filter(lab_name=laboratory)
            # .values('serial', 'name__type_name', 'brand__brand_name', 'lab_name', 'image', 'upcoming_maintenance', 'necessary_maintenance')

        if request.GET.get('q'):
            query = request.GET.get('q')
            results = results.filter(
                Q(serial__icontains=query) | 
                Q(name__type_name__icontains=query) | 
                Q(brand__brand_name__icontains=query)
            )

        laboratory = Labs.objects.get(id=laboratory)
        print("results", results)

        paginator = Paginator(results, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        up_to_date = results.filter(necessary_maintenance='AD').count()
        expiring = results.filter(necessary_maintenance='PV').count()
        expired = results.filter(necessary_maintenance='VE').count()

        return render(request, 'storage/search.html', {
            'results': page_obj,
            'page_obj': page_obj,
            'laboratory': laboratory,
            'machinary_type': machinary,
            "up_to_date": up_to_date,
            "expiring": expiring,
            "expired": expired,
        })