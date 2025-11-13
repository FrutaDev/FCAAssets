from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="landing-page"),
    path('machinary-detail/<slug:serial>', views.MachinaryDetail.as_view(), name="machinary-detail"),
    path('maintenance-detail/<slug:id>',views.MaintenanceDetail.as_view(), name="maintenance-detail"),
    path('maintenance-file/<slug:id>', views.MaintenanceFileDownload.as_view(), name="maintenance-file-download"),
    path('create-maintenance/', views.CreateMaintenance.as_view(), name="create-maintenance"),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),

]