from django.utils import timezone
from django.contrib.auth import authenticate
from datetime import timedelta

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.db.models import Count

from .models import Patient, Appointment
from .serializers import PatientSerializer, AppointmentSerializer
from .permissions import IsStaffOrReadOnly
from clinic_api.utils import success_response, error_response


class PatientViewSet(viewsets.ModelViewSet):

    serializer_class = PatientSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        return Patient.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data, message="Patients fetched .")

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            return error_response(message="Patient not found.", http_status=404)

        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message="Patient fetched .")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                data=serializer.data,
                message="Patient created .",
                http_status=201
            )
        return error_response(message="Validation failed.", data=serializer.errors, http_status=400)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except Exception:
            return error_response(message="Patient not found.", http_status=404)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Patient updated .")
        return error_response(message="Validation failed.", data=serializer.errors, http_status=400)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            return error_response(message="Patient not found.", http_status=404)

        instance.delete()
        return success_response(message="Patient deleted .")


class AppointmentViewSet(viewsets.ModelViewSet):

    serializer_class = AppointmentSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = Appointment.objects.all()
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        patient_id = self.request.query_params.get('patient_id', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data, message="Appointments fetched .")

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            return error_response(message="Appointment not found.", http_status=404)

        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message="Appointment fetched .")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                data=serializer.data,
                message="Appointment created .",
                http_status=201
            )
        return error_response(message="Validation failed.", data=serializer.errors, http_status=400)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except Exception:
            return error_response(message="Appointment not found.", http_status=404)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Appointment updated .")
        return error_response(message="Validation failed.", data=serializer.errors, http_status=400)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            return error_response(message="Appointment not found.", http_status=404)

        instance.delete()
        return success_response(message="Appointment deleted .")


class StatsView(APIView):
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request):
        total_patients = Patient.objects.count()
        total_appointments = Appointment.objects.count()
        status_counts_qs = (
            Appointment.objects
            .values('status')
            .annotate(count=Count('id'))
        )
        status_counts = {item['status']: item['count'] for item in status_counts_qs}
        data = {
            "total_patients": total_patients,
            "total_appointments": total_appointments,
            "appointments_by_status": {
                "Pending": status_counts.get("Pending", 0),
                "Confirmed": status_counts.get("Confirmed", 0),
                "Cancelled": status_counts.get("Cancelled", 0),
            }
        }
        return success_response(data=data, message="Stats fetched .")


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return error_response(
                message="Username and password are required.",
                http_status=400
            )
        user = authenticate(username=username, password=password)
        if user is None:
            return error_response(
                message="Invalid credentials. Please check username and password.",
                http_status=400
            )
        token, created = Token.objects.get_or_create(user=user)
        return success_response(
            data={"token": token.key},
            message="Login successful."
        )
