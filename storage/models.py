from django.db import models
from datetime import timedelta

# Create your models here.

#Laboratorios disponibles
class Labs(models.Model):
    lab_name = models.CharField(max_length=50)

    def __str__(self):
        return self.lab_name

#Modelo de inventario
class Storage(models.Model):
    serial = models.CharField(max_length=50, default="")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="storage/images",default="", null=True, blank=True)
    lab_name = models.ForeignKey('Labs', related_name='labs', on_delete=models.CASCADE)
    acquisition_date = models.DateField(null=True, blank=True)



    def __str__(self):
        return self.name

#Proveedores de mantenimiento
class Suplier(models.Model):
    name_provider = models.CharField(max_length=100)

    def __str__(self):
        return self.name_provider

#Modelo de mantenimientos
class Maintenance(models.Model):
    machinary_maintenance = models.ForeignKey(Storage, on_delete=models.CASCADE)
    maintenance_provider = models.ForeignKey(Suplier, on_delete=models.SET_NULL, null=True)
    maintenance_image = models.ImageField(upload_to="storage/images",default="", null=True, blank=True)
    maintenance_date = models.DateField()
    upcoming_maitenance = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.machinary_maintenance} último mantenimiento {self.maintenance_date}"
    
    def save(self,*args, **kwargs):
        if not self.upcoming_maitenance:
            self.upcoming_maitenance = self.maintenance_date + timedelta(days=365)
        super().save(*args, **kwargs)