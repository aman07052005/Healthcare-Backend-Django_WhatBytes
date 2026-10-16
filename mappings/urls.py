from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PatientDoctorMappingViewSet
from .views_extra import PatientMappingsByPatientView

router = DefaultRouter()
router.register("", PatientDoctorMappingViewSet, basename="mapping")
urlpatterns = [
    path("<int:patient_id>/", PatientMappingsByPatientView.as_view(), name="patient-mappings"),
] + router.urls
