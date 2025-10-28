from django.contrib import admin
from .models import Labs, Storage, Maintenance, Suplier

# Register your models here.

admin.site.register(Maintenance)
admin.site.register(Suplier)
admin.site.register(Labs)
admin.site.register(Storage)