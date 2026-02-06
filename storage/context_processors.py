from .models import Labs, Types

def navigation_filters(request):
    """
    Provides available laboratories and machinery types to all templates
    for the global navigation header.
    """
    return {
        'available_laboratories': Labs.objects.values_list('lab_name', 'id').distinct(),
        'available_machinary_types': Types.objects.values_list('type_name', 'id').distinct(),
    }
