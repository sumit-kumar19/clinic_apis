from django.db import models


class Patient(models.Model):
    # storing patientinfo
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=10)  
    blood_group = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments')
    doctor_name = models.CharField(max_length=200)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.patient.name} - {self.doctor_name}"
