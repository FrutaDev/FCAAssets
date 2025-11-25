from django.contrib import admin
from .models import Labs, Storage, Maintenance, Suplier, Types, Brand

# Register your models here.

class StorageAdmin(admin.ModelAdmin):
    list_display = ('serial', 'model', 'lab', 'necessary_maintenance')
    search_fields = ('serial', 'model', 'lab__name_lab')
    list_filter = ('necessary_maintenance', 'lab')

class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('machinary_maintenance', 'maintenance_date', 'is_approved', 'maintenance_provider')
    search_fields = ('machinary_maintenance__serial', 'maintenance_provider__name_provider')
    list_filter = ('is_approved', 'maintenance_date')

admin.site.register(Maintenance)
admin.site.register(Suplier)
admin.site.register(Labs)
admin.site.register(Storage)
admin.site.register(Types)
admin.site.register(Brand)