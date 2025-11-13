from django import forms 
from .models import Maintenance

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = [
            'machinary_maintenance',
            'maintenance_date',
            'maintenance_provider',
            'maintenance_image',
            'maintenance_file',
        ]
        error_messages = {
            'machinary_maintenance': {
                'required': "El campo de maquinaria es obligatorio.",
            },
            'maintenance_date': {
                'required': "La fecha de mantenimiento es obligatoria.",
            },
            'maintenance_provider': {
                'required': "El proveedor de mantenimiento es obligatorio.",
            },
        }
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }