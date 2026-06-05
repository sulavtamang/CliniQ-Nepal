from django.urls import path
from clinics.views import DoctorListView

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list')
]
