from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="landing-page"),
    path('search/', views.Search.as_view(), name="search"),
    path('machinary-detail/<slug:serial>', views.MachinaryDetail.as_view(), name="machinary-detail"),
    path('maintenance-detail/<slug:id>',views.MaintenanceDetail.as_view(), name="maintenance-detail"),
    path('maintenance-file/<slug:id>', views.MaintenanceFileDownload.as_view(), name="maintenance-file-download"),
    path('create-maintenance/', views.CreateMaintenance.as_view(), name="create-maintenance"),
    path('create-machinary/', views.CreateMachinary.as_view(), name="create-machinary"),
    path('edit-machinary/<slug:serial>/', views.EditMachinary.as_view(), name="edit-machinary"),
    path('api/create-lab/', views.CreateLab.as_view(), name="api-create-lab"),
    path('api/create-brand/', views.CreateBrand.as_view(), name="api-create-brand"),
    path('api/create-type/', views.CreateType.as_view(), name="api-create-type"),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),

]