from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PatientCheckIn, Patient, User, DoctorPatientInfo, Doctor, Nurse, NursePatientInfo
from django.forms import widgets
from members.models import User
from .models import NursePatientInfo, TestType

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

class PatientCheckInForm(forms.ModelForm):
    date_time = forms.DateTimeField(
        widget=widgets.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(profile__role='DOC')
        self.fields['nurse'].queryset = User.objects.filter(profile__role='NUR')

    class Meta:
        model = PatientCheckIn
        fields = ['date_time', 'patient', 'doctor', 'nurse']

class NursePatientInfoForm(forms.ModelForm):
    test_types = forms.ModelMultipleChoiceField(
        queryset=TestType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = NursePatientInfo
        fields = ['heart_rate', 'blood_pressure', 'test_types', 'notes', 'dischargeNotes']

class DoctorPatientInfoForm(forms.ModelForm):
    class Meta:
        model = DoctorPatientInfo
        fields = ['heart_rate', 'blood_pressure', 'test_type', 'notes', 'prescription', 'diagnoses', 'dischargeNotes']

class CaseForm(forms.ModelForm):
    class Meta:
        model = PatientCheckIn
        fields = ['patient', 'status']
