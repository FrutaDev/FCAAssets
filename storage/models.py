from django.db import models
from datetime import timedelta, date

# Create your models here.

#Laboratorios disponibles
class Labs(models.Model):
    lab_name = models.CharField(max_length=50)

    def __str__(self):
        return self.lab_name

#Modelo de inventario
class Storage(models.Model):
    serial = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to="storage/images", null=True, blank=True)
    acquisition_date = models.DateField(null=True, blank=True)
    name = models.ForeignKey("Types", on_delete=models.CASCADE, related_name="type")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, null=True, related_name="brand")
    lab_name = models.ForeignKey('Labs', related_name='labs', on_delete=models.CASCADE)
    necessary_maintenance = models.BooleanField(default=False)

    def __str__(self):
        return self.name.type_name




class Types(models.Model):
    type_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.type_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.brand_name

#Proveedores de mantenimiento
class Suplier(models.Model):
    name_provider = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name_provider

#Modelo de mantenimientos
class Maintenance(models.Model):
    machinary_maintenance = models.ForeignKey("Storage", on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    maintenance_provider = models.ForeignKey("Suplier", on_delete=models.SET_NULL, null=True)
    maintenance_image = models.ImageField(upload_to="storage/images",null=True, blank=True)
    maintenance_file = models.FileField(upload_to="storage/files", null=True, blank=True)
    upcoming_maintenance = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.machinary_maintenance} último mantenimiento {self.maintenance_date}"

    def save(self,*args, **kwargs):
        if not self.upcoming_maintenance:
            self.upcoming_maintenance = self.maintenance_date + timedelta(days=365)
        super().save(*args, **kwargs)