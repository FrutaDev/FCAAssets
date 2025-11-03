from django.urls import path 
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="landing-page"),
    path('machinary-detail/<slug:serial>', views.MachinaryDetail.as_view(), name="machinary-detail")
]