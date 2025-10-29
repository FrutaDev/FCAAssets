from django.contrib import admin
from .models import Labs, Storage, Maintenance, Suplier, Types, Brand

# Register your models here.

admin.site.register(Maintenance)
admin.site.register(Suplier)
admin.site.register(Labs)
admin.site.register(Storage)
admin.site.register(Types)
admin.site.register(Brand)