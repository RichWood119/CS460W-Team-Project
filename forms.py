from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PatientCheckIn, User, DoctorPatientInfo
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PatientCheckInForm(forms.ModelForm):

    class Meta:
        model = PatientCheckIn
        fields = ['date_time', 'patient', 'doctor', 'nurse']

class DoctorPatientInfoForm(forms.ModelForm):
    heart_rate = forms.CharField(max_length=10, label='Heart Rate (BPM)')
    blood_pressure = forms.CharField(max_length=10, label='Blood Pressure (i.e, 120/80)')

    test_type = forms.CharField(max_length=10, choices=DoctorPatientInfo.TEST_CHOICES)

    notes = forms.CharField(widget=forms.Textarea)
    prescriptions = forms.CharField(widget=forms.Textarea)
    diagnoses = forms.CharField(widget=forms.Textarea)
    discharge_notes = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = DoctorPatientInfo
        fields = ['heart_rate', 'blood_pressure', 'test_type',
                  'notes', 'prescriptions', 'diagnoses', 'discharge_notes']

