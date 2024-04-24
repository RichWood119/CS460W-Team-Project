from django.contrib import admin
from .models import DoctorPatientInfo, Patient, Visit, Diagnosis, TestResult, Medication, Appointment
from .models import User, AdmittingStaff, BillingStaff, Doctor, Nurse, Profile, PatientCheckIn

admin.site.register(User)
admin.site.register(AdmittingStaff)
admin.site.register(BillingStaff)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Appointment)
admin.site.register(Profile)
admin.site.register(PatientCheckIn)
admin.site.register(DoctorPatientInfo)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    search_fields = ('last_name', )

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_filter = ('discharge_status', 'doctor')

    # Inline definitions
    class DiagnosisInline(admin.TabularInline):
        model = Diagnosis
        extra = 1  # Provide space for an extra, empty row

    class TestResultInline(admin.TabularInline):
        model = TestResult
        extra = 1

    class MedicationInline(admin.TabularInline):
        model = Medication
        extra = 1

    inlines = [DiagnosisInline, TestResultInline, MedicationInline]
