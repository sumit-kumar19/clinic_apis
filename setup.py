import os
import sys
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic_api.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command
from patients.models import Patient, Appointment
from rest_framework.authtoken.models import Token
from django.utils import timezone


def run_setup():
    print("=" * 50)
    print("  clinic api - setup skript")
    print("=" * 50)

    print("\n[1/5] running migartions...")
    call_command('migrate', verbosity=0)
    print("  ✓ Migrations done.")

    print("\n[2/5] creating superuser...")
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@clinic.com'
        )
        Token.objects.get_or_create(user=admin)
        print("  ✓ admin created: admin / admin123")
    else:
        print("  → admin already exists.")

    print("\n[3/5] creating regular user...")
    if not User.objects.filter(username='user1').exists():
        user = User.objects.create_user(
            username='user1',
            password='user123',
            email='user1@clinic.com',
            is_staff=False
        )
        Token.objects.get_or_create(user=user)
        print("  ✓ user created: user1 / user123")
    else:
        print("  → user already exists.")

    print("\n[4/5] adding patints...")
    if Patient.objects.count() == 0:
        p1 = Patient.objects.create(
            name="Rahul Sharma",
            age=32,
            gender="Male",
            contact_number="9876543210",
            blood_group="A+"
        )
        p2 = Patient.objects.create(
            name="Priya Patel",
            age=28,
            gender="Female",
            contact_number="8765432109",
            blood_group="B+"
        )
        p3 = Patient.objects.create(
            name="Amit Verma",
            age=45,
            gender="Male",
            contact_number="7654321098",
            blood_group="O-"
        )
        print("  ✓ Created 3 patients.")
    else:
        print("  → Patients already exist, skipping.")
        p1, p2, p3 = Patient.objects.all()[:3]

    print("\n[5/5] adding appointements...")
    if Appointment.objects.count() == 0:
        now = timezone.now()
        Appointment.objects.create(
            patient=p1,
            doctor_name="Dr. Anil Kumar",
            appointment_date=now + timedelta(days=2),
            reason="Routine checkup",
            status="Confirmed"
        )
        Appointment.objects.create(
            patient=p2,
            doctor_name="Dr. Sunita Rao",
            appointment_date=now + timedelta(days=5),
            reason="Fever and cold",
            status="Pending"
        )
        Appointment.objects.create(
            patient=p3,
            doctor_name="Dr. Anil Kumar",
            appointment_date=now - timedelta(days=3),
            reason="Back pain follow-up",
            status="Cancelled"
        )
        print("  ✓ Created 3 appointements.")
    else:
        print("  → Appointements already exist.")

    print("\n" + "=" * 50)
    print("  setup complte!")
    print("=" * 50)
    print("\nrun server:")
    print("  python manage.py runserver")
    print("\nadmin: http://127.0.0.1:8000/admin/ (admin/admin123)")
    print("\napi login: POST /api/auth/login/")
    print('\n')


if __name__ == '__main__':
    run_setup()
