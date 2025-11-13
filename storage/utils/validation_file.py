from django.core.exceptions import ValidationError

def validate_pdf(file):
    if not file.name.lower().endswith('.pdf'):
        raise ValidationError("Solo se permiten archivos en formato PDF.")