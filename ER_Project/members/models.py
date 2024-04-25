import datetime, random
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

def generate_next_patient_id():
    last_patient = Patient.objects.all().order_by('-patientID').first()
    if not last_patient:
        return 1000
    return last_patient.patientID + 1

class Patient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    emergency_contact_1_name = models.CharField(max_length=50)
    emergency_contact_1_relationship = models.CharField(max_length=50)
    emergency_contact_1_phone = models.CharField(max_length=20)
    emergency_contact_2_name = models.CharField(max_length=50)
    emergency_contact_2_relationship = models.CharField(max_length=50)
    emergency_contact_2_phone = models.CharField(max_length=20)
    reason_for_visit = models.TextField()
    allergies = models.TextField()
    current_medical_problems = models.TextField()
    current_medications = models.TextField()
    insurance = models.BooleanField()
    def __str__(self):
      return f"{self.first_name} {self.last_name} (id: {self.patientID})"

class User(AbstractUser):
    DOCTOR = 'DOC'
    NURSE = 'NUR'
    ADMITTING_STAFF = 'ADM'
    BILLING_STAFF = 'BIL'
    ROLE_CHOICES = (
        (DOCTOR, 'Doctor'),
        (NURSE, 'Nurse'),
        (ADMITTING_STAFF, 'Admitting Staff'),
        (BILLING_STAFF, 'Billing Staff'),
    )
    role = models.CharField(max_length=4, choices=ROLE_CHOICES, default='ADM')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=4, choices=User.ROLE_CHOICES)

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

class PatientCheckIn(models.Model):
    date_time = models.DateTimeField()
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_checkins')
    nurse = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='nurse_checkins')
    status = models.CharField(max_length=20, choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Open')

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Nurse(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class AdmittingStaff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class BillingStaff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class TestType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class NursePatientInfo(models.Model):
    heart_rate = models.CharField(max_length=10)
    blood_pressure = models.CharField(max_length=10)
    test_types = models.ManyToManyField(TestType)
    notes = models.TextField()
    dischargeNotes = models.TextField()
    patient_check_in = models.ForeignKey('members.PatientCheckIn', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.datetime.now)

class TestResult(models.Model):
    nurse_patient_info = models.ForeignKey(NursePatientInfo, on_delete=models.CASCADE, related_name='test_results')
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    result = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def generate_random_result(self):
        results = ['Normal', 'Abnormal']
        self.result = random.choice(results)
        self.save()

    def __str__(self):
        return f"{self.test_type.name} - {self.result}"

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
    dischargeNotes = models.TextField(default="")
    patient_check_in = models.ForeignKey(PatientCheckIn, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.datetime.now)

class Diagnosis(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    description = models.TextField()

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
