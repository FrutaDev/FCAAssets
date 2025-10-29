from django.shortcuts import render
from django.views.generic.base import View
from .models import Maintenance

# Create your views here.

class Index(View):
    def get(self, request):
        all_maitenances = Maintenance.objects.all()
        requires = Maintenance.objects.filter(maintenance_neccesary=True).count()
        not_requires = Maintenance.objects.filter(maintenance_neccesary=False).count()

        return render(request, "storage/index.html", {
            "maintenances": all_maitenances,
            "requires": requires,
            "not_requires": not_requires
        })