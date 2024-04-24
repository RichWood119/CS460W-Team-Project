from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PatientCheckIn, Patient, User, DoctorPatientInfo, Doctor, Nurse, NursePatientInfo
from django.forms import widgets
from members.models import User

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

TEST_CHOICES = [
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
]

class NursePatientInfoForm(forms.ModelForm):
    class Meta:
        model = NursePatientInfo
        fields = ['heart_rate', 'blood_pressure', 'test_type', 'notes']

class DoctorPatientInfoForm(forms.ModelForm):
    heart_rate = forms.CharField(max_length=10, label='Heart Rate (BPM)')
    blood_pressure = forms.CharField(max_length=10, label='Blood Pressure (ex: 120/80)')

    test_type = forms.ChoiceField(choices=TEST_CHOICES)

    notes = forms.CharField(widget=forms.Textarea)
    prescriptions = forms.CharField(widget=forms.Textarea)
    diagnoses = forms.CharField(widget=forms.Textarea)
    discharge_notes = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = DoctorPatientInfo
        fields = ['heart_rate', 'blood_pressure', 'test_type',
                  'notes', 'prescriptions', 'diagnoses', 'discharge_notes']
