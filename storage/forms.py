from django import forms 
from .models import Maintenance, Storage

class StorageModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.serial} - {obj.name} ({obj.brand})"

class MaintenanceForm(forms.ModelForm):
    machinary_maintenance = StorageModelChoiceField(
        queryset=Storage.objects.all(),
        label="Serial del equipo",
        error_messages={'required': "El campo de maquinaria es obligatorio."}
    )

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

class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage # type: ignore
        fields = [
            'serial',
            'image',
            'acquisition_date',
            'name',
            'brand',
            'lab_name',
            'floor',
            'upcoming_maintenance',
        ]
        labels = {
            'name': 'Tipo de maquinaria',
            'brand': 'Marca',
            'lab_name': 'Laboratorio',
        }
        widgets = {
            'acquisition_date': forms.DateInput(attrs={'type': 'date'}),
            'upcoming_maintenance': forms.DateInput(attrs={'type': 'date'}),
        }
