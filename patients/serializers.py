from rest_framework import serializers
from .models import Patient, Appointment


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = '__all__'

    def validate_age(self, value):
        return value

    def validate_contact_number(self, value):

        if not value.isdigit():
            raise serializers.ValidationError("Contact number must contain only digits.")
        return value


class AppointmentSerializer(serializers.ModelSerializer):

    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
