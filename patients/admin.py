from django.contrib import admin
from .models import Patient, Appointment


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    # let admin see and search patients
    list_display = ['id', 'name', 'age', 'gender', 'blood_group', 'contact_number', 'created_at']
    search_fields = ['name', 'contact_number', 'blood_group']
    list_filter = ['gender', 'blood_group']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor_name', 'appointment_date', 'status']
    search_fields = ['patient__name', 'doctor_name', 'reason']
    list_filter = ['status', 'doctor_name']
