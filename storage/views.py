from django.shortcuts import render
from django.views.generic.base import View
from .models import Maintenance

# Create your views here.

class Index(View):
    def get(self, request):
        all_maitenances = Maintenance.objects.all()
        return render(request, "storage/index.html", {
            # "maitenances": maitenance
        })