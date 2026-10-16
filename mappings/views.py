from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotFound
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer

class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(patient__owner=self.request.user).select_related("patient", "doctor")

    def get_object(self):
        # Default lookup is mapping ID; patient-specific GET is handled by a separate action URL below.
        return super().get_object()
