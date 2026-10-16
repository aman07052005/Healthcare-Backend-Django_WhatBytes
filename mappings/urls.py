
from django.urls import path
from .views import PatientDoctorMappingViewSet
from .views_extra import PatientMappingsByPatientView

mapping_list = PatientDoctorMappingViewSet.as_view({
    "get": "list",
    "post": "create",
})

urlpatterns = [
    path("", mapping_list, name="mapping-list"),
    path("<int:patient_id>/", PatientMappingsByPatientView.as_view(), name="patient-mappings"),
]
