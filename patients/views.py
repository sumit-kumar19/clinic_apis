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
    # handles create, read, update, delete for patients

    serializer_class = PatientSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        # filter by search query param
        queryset = Patient.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset

    def list(self, request, *args, **kwargs):
        # returns list of all patients
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data, message="Patients fetched successfully.")

    def retrieve(self, request, *args, **kwargs):
        # returns one patient by id
        try:
            instance = self.get_object()
        except Exception:
            return error_response(message="Patient not found.", http_status=404)

        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message="Patient fetched successfully.")

    def create(self, request, *args, **kwargs):
        # adds new patient to database
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                data=serializer.data,
                message="Patient created successfully.",
                http_status=201
            )
        return error_response(message="Validation failed.", data=serializer.errors, http_status=400)

    def update(self, request, *args, **kwargs):
        # changes patient info
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except Exception:
            return error_response(message="Patient not found.", http_status=404)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Patient updated successfully.")
        return error_response(message="Validation failed.", data=serializer.errors, http_status=400)

    def destroy(self, request, *args, **kwargs):
        # removes patient from database
        try:
            instance = self.get_object()
        except Exception:
            return error_response(message="Patient not found.", http_status=404)

        instance.delete()
        return success_response(message="Patient deleted successfully.")


class AppointmentViewSet(viewsets.ModelViewSet):
    # handles create, read, update, delete for appointements

    serializer_class = AppointmentSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        # filter by status and patient id from query params
        queryset = Appointment.objects.all()
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        patient_id = self.request.query_params.get('patient_id', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        return queryset

    def list(self, request, *args, **kwargs):
        # returns all appointements
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data, message="Appointments fetched successfully.")

    def retrieve(self, request, *args, **kwargs):
        # returns one appointement by id
        try:
            instance = self.get_object()
        except Exception:
            return error_response(message="Appointment not found.", http_status=404)

        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message="Appointment fetched successfully.")

    def create(self, request, *args, **kwargs):
        # adds new appointement
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                data=serializer.data,
                message="Appointment created successfully.",
                http_status=201
            )
        return error_response(message="Validation failed.", data=serializer.errors, http_status=400)

    def update(self, request, *args, **kwargs):
        # changes appointement details
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except Exception:
            return error_response(message="Appointment not found.", http_status=404)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Appointment updated successfully.")
        return error_response(message="Validation failed.", data=serializer.errors, http_status=400)

    def destroy(self, request, *args, **kwargs):
        # removes appointement
        try:
            instance = self.get_object()
        except Exception:
            return error_response(message="Appointment not found.", http_status=404)

        instance.delete()
        return success_response(message="Appointment deleted successfully.")

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming(self, request):
        # returns appointements for next 7 days
        now = timezone.now()
        next_7_days = now + timedelta(days=7)
        upcoming_appointments = Appointment.objects.filter(
            appointment_date__gte=now,
            appointment_date__lte=next_7_days
        ).order_by('appointment_date')
        serializer = self.get_serializer(upcoming_appointments, many=True)
        return success_response(
            data=serializer.data,
            message=f"Found {upcoming_appointments.count()} upcoming appointments."
        )


class StatsView(APIView):
    # returns statistics about patients and appointements
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
        return success_response(data=data, message="Stats fetched successfully.")


class LoginView(APIView):
    # authenticates user and returns token
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
