from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from patients.models import Patient

class PatientMappingsByPatientView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, patient_id):
        if not Patient.objects.filter(id=patient_id, owner=request.user).exists():
            raise NotFound("Patient not found.")
        mappings = PatientDoctorMapping.objects.filter(
            patient_id=patient_id, patient__owner=request.user
        ).select_related("patient", "doctor")
        return Response(PatientDoctorMappingSerializer(mappings, many=True, context={"request": request}).data)

    def delete(self, request, patient_id):
        # The assignment uses the same URL shape for patient-specific GET and mapping-ID DELETE.
        # DELETE interprets the path integer as a mapping ID.
        try:
            mapping = PatientDoctorMapping.objects.select_related("patient").get(
                id=patient_id, patient__owner=request.user
            )
        except PatientDoctorMapping.DoesNotExist:
            raise NotFound("Mapping not found.")
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
