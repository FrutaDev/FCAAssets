from django.urls import path 
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="landing-page"),
    path('machinary-detail/<slug:serial>', views.MachinaryDetail.as_view(), name="machinary-detail"),
    path('maintenance-detail/<slug:id>',views.MaintenanceDetail.as_view(), name="maintenance-detail"),
    path('maintenance-file/<slug:id>', views.MaintenanceFileDownload.as_view(), name="maintenance-file-download"),
]