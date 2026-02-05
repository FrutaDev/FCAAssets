from django.db import models
from datetime import timedelta, date
from storage.utils.validation_file import validate_pdf
from django.core.validators import MaxValueValidator

class Labs(models.Model):
    lab_name = models.CharField(max_length=50)

    def __str__(self):
        return self.lab_name

class Storage(models.Model):
    AL_DIA = 'AD'
    POR_VENCER = 'PV'
    VENCIDO = 'VE'

    MAINTENANCE_STATUS_CHOICES = [
        (AL_DIA, 'Al día'),
        (POR_VENCER, 'Por vencer'),
        (VENCIDO, 'Vencido'),
    ]
    serial = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to="storage/images/storage", null=True, blank=True)
    acquisition_date = models.DateField(null=True, blank=True)
    name = models.ForeignKey("Types", on_delete=models.CASCADE, related_name="type")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, null=True, related_name="brand")
    lab_name = models.ForeignKey('Labs', related_name='labs', on_delete=models.CASCADE)
    floor = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(9)])
    necessary_maintenance = models.CharField(max_length=2, choices=MAINTENANCE_STATUS_CHOICES, default=AL_DIA)
    upcoming_maintenance = models.DateField(blank=True, null=True)
    
    email_sent_30_days = models.BooleanField(default=False)
    email_sent_7_days = models.BooleanField(default=False)
    email_sent_due = models.BooleanField(default=False)


    def __str__(self):
        return self.name.type_name
    
    def save(self,*args, **kwargs):
        today = date.today()
        if not self.acquisition_date:
            self.acquisition_date = today
        
        if self.upcoming_maintenance is None:
            self.upcoming_maintenance = self.acquisition_date + timedelta(days=365)
            self.necessary_maintenance = "AD" if self.upcoming_maintenance - today > timedelta(days=30) else "VE" if self.upcoming_maintenance - today <= timedelta(days=0) else "PV"
        else:
            self.necessary_maintenance = "AD" if self.upcoming_maintenance - today > timedelta(days=30) else "VE" if self.upcoming_maintenance - today <= timedelta(days=0) else "PV"
        

        super().save(*args, **kwargs)




class Types(models.Model):
    type_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.type_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.brand_name

class Suplier(models.Model):
    name_provider = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name_provider

class Maintenance(models.Model):
    machinary_maintenance = models.ForeignKey("Storage", on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    maintenance_provider = models.ForeignKey("Suplier", on_delete=models.SET_NULL, null=True)
    maintenance_image = models.ImageField(upload_to="storage/images/maintenances",null=True, blank=True)
    maintenance_file = models.FileField(upload_to="storage/files", null=True, blank=True, validators=[validate_pdf])
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.machinary_maintenance} mantenimiento realizado por {self.maintenance_provider} el {self.maintenance_date} estatus {'Aprobado' if self.is_approved else 'Pendiente'}"
