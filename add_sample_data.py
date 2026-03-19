import os
import sys
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic_api.settings')
django.setup()

from patients.models import Patient, Appointment
from django.utils import timezone


def add_indian_data():


    patients_data = [
        {
            "name": "rajesh kumar",
            "age": 35,
            "gender": "Male",
            "contact_number": "9876543210",
            "blood_group": "A+"
        },
        {
            "name": "priya sharma",
            "age": 28,
            "gender": "Female",
            "contact_number": "8765432109",
            "blood_group": "B+"
        },
        {
            "name": "amit patel",
            "age": 42,
            "gender": "Male",
            "contact_number": "7654321098",
            "blood_group": "O-"
        },
        {
            "name": "anjali verma", 
            "age": 31,
            "gender": "Female",
            "contact_number": "9988776655",
            "blood_group": "AB+"
        },
        {
            "name": "vikas singh",
            "age": 45,
            "gender": "Male",
            "contact_number": "9123456789",
            "blood_group": "A-"
        },
        {
            "name": "neha gupta",
            "age": 26,
            "gender": "Female",
            "contact_number": "8812345678",
            "blood_group": "B-"
        },
        {
            "name": "suresh reddy",  
            "age": 55,
            "gender": "Male",
            "contact_number": "7712345678",
            "blood_group": "O+"
        },
        {
            "name": "meera chauhan", 
            "age": 32,
            "gender": "Female",
            "contact_number": "9512345678",
            "blood_group": "AB-"
        },
    ]

    print("\n[1/2] adding patints...")
    created_count = 0
    for patient_data in patients_data:
        patient, created = Patient.objects.get_or_create(
            contact_number=patient_data["contact_number"],
            defaults=patient_data
        )
        if created:
            created_count += 1
            print(f"  ✓ {patient_data['name']}")

    print(f"  Total patients added: {created_count}")

    all_patients = Patient.objects.all()

    doctors = [
        "dr. raghav sharma",  
        "dr. priya nair",      
        "dr. amit kulkarni",   
        "dr. shreya dutta",    
        "dr. vikram singh",    
    ]

    print("\n[2/2] adding appointements...")
    now = timezone.now()
    created_count = 0

    for i, patient in enumerate(all_patients):
        for j in range(min(3, len(doctors))):
            appointment_date = now + timedelta(days=2+i+j, hours=10)
            status_choice = ["Pending", "Confirmed", "Cancelled"][j % 3]

            appointment, created = Appointment.objects.get_or_create(
                patient=patient,
                appointment_date=appointment_date,
                doctor_name=doctors[j % len(doctors)],
                defaults={
                    "reason": reasons[(i + j) % len(reasons)],
                    "status": status_choice,
                }
            )
            if created:
                created_count += 1
                print(f"  ✓ {patient.name} → {doctors[j % len(doctors)]}")

    print(f"  Total appointments added: {created_count}")

    print("\n" + "=" * 60)
    print("  data added sucessfully!")
    print("=" * 60)
    print("\ntry these api calls:")
    print("  GET http://127.0.0.1:8000/api/patients/")
    print("  GET http://127.0.0.1:8000/api/appointments/")
    print("  GET http://127.0.0.1:8000/api/stats/")
    print("\nuse header: Authorization: Token <your-token>")
    print("\n")


if __name__ == '__main__':
    add_indian_data()
