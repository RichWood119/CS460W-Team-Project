#add these models into the project then do python manage.py makemigrations and python manage.py migrate (should work)
import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,
from .forms import DoctorPatientInfoForm

class PatientCheckIn(models.Model):
    date_time = models.DateTimeField()
    patient = models.ForeignKey('members.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_checkins')
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nurse_checkins')
    status = models.CharField(max_length=20, choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Open')

class NursePatientInfo(models.Model):
    heart_rate = models.CharField(max_length=10)
    blood_pressure = models.CharField(max_length=10)
    test_type = models.CharField(max_length=10, choices=[
        ('XRY', 'X-Ray'),
        ('CT', 'CT Scan'),
        ('MRI', 'MRI'),
        ('RBC', 'Red Blood Cell'),
        ('WBC', 'White Blood Cell'),
        ('LVF', 'Liver Function'),
        ('RNF', 'Renal Function'),
        ('ELCT', 'Electrolyte Test'),
        ('UNT', 'Urinary Test'),
        ('ST', 'Stool Test'),
    ])
    notes = models.TextField()
    patient_check_in = models.ForeignKey('members.PatientCheckIn', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.datetime.now)

class DoctorPatientInfo(models.Model):
    heart_rate = models.CharField(max_length=10)
    blood_pressure = models.CharField(max_length=10)
    test_type = models.CharField(max_length=10, choices=[
        ('XRY', 'X-Ray'),
        ('CT', 'CT Scan'),
        ('MRI', 'MRI'),
        ('RBC', 'Red Blood Cell'),
        ('WBC', 'White Blood Cell'),
        ('LVF', 'Liver Function'),
        ('RNF', 'Renal Function'),
        ('ELCT', 'Electrolyte Test'),
        ('UNT', 'Urinary Test'),
        ('ST', 'Stool Test'),
    ])
    notes = models.TextField()
    prescription = models.TextField()
    diagnoses = models.TextField()
    dischargeNotes = models.TextField()
    patient_check_in = models.ForeignKey(PatientCheckIn, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
