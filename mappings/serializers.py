from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())

    class Meta:
        model = PatientDoctorMapping
        fields = ("id", "patient", "patient_name", "doctor", "doctor_name", "created_at")
        read_only_fields = ("id", "created_at")

    def validate(self, attrs):
        request = self.context.get("request")
        patient = attrs.get("patient", getattr(self.instance, "patient", None))
        doctor = attrs.get("doctor", getattr(self.instance, "doctor", None))
        if request and patient and patient.owner_id != request.user.id:
            raise serializers.ValidationError({"patient": "You can only assign doctors to your own patients."})
        if self.instance and patient and doctor:
            exists = PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exclude(pk=self.instance.pk).exists()
        elif patient and doctor:
            exists = PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists()
        else:
            exists = False
        if exists:
            raise serializers.ValidationError("This doctor is already assigned to this patient.")
        return attrs
