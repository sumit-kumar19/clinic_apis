from rest_framework import serializers
from .models import Patient, Appointment


class PatientSerializer(serializers.ModelSerializer):
    # convert patient to json and validate

    class Meta:
        model = Patient
        fields = '__all__'

    def validate_age(self, value):
        if value < 0 or value > 120:
            raise serializers.ValidationError("Age must be between 0 and 120.")
        return value

    def validate_contact_number(self, value):
        # validate phone number
        if not value.isdigit():
            raise serializers.ValidationError("Contact number must contain only digits.")
        if len(value) != 10:
            raise serializers.ValidationError("Contact number must be exactly 10 digits.")
        return value


class AppointmentSerializer(serializers.ModelSerializer):
    #  appointement to json

    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
