from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

def generate_next_patient_id():
    last_patient = Patient.objects.all().order_by('-patientID').first()
    if not last_patient:
        return 1000
    return last_patient.patientID + 1

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patientID = models.AutoField(
        default=generate_next_patient_id,
        primary_key=True,
        serialize=False,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    other_info = models.TextField(blank=True)
    allergies = models.TextField(blank=True)

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    chief_complaint = models.TextField()
    triage_notes = models.TextField(blank=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    discharge_status = models.CharField(max_length=50, choices=[
        ('ADM', 'Admitted'),
        ('DIS', 'Discharged'),
        ('OTH', 'Other')
    ])

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    notes = models.TextField(blank=True)

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Nurse(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Diagnosis(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    description = models.TextField()

class TestResult(models.Model):
    test_type = models.CharField(max_length=3, choices=[
        ('XRY', 'X-Ray'),
        ('CT', 'CT Scan'),
        ('MRI', 'MRI'),
    ])
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    result = models.TextField(blank=True)  # Or a FileField to upload images

class Medication(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    route = models.CharField(max_length=3, choices=[
        ('ORA', 'Oral'),
        ('IV', 'Intravenous'),
        ('SC', 'Subcutaneous')
    ])
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    prescription_date = models.DateTimeField(auto_now_add=True)

