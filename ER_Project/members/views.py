from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .forms import DoctorPatientInfoForm, RegistrationForm, PatientCheckInForm, NursePatientInfoForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView
from .models import Doctor, Nurse, Patient, Profile, PatientCheckIn, NursePatientInfo, DoctorPatientInfo, TestResult
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'login.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('dashboard')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def doctor_form(request):
    return render(request, 'doctor_form.html')

def patient_list(request):
    patients = Patient.objects.all() #fetch all patients
    context = {'patients': patients}
    return render(request, 'patient_list.html', context)

def new_patient(request):
    print("new_patient view accessed!")
    if request.method == 'POST':
        form_data = request.POST

        try:
            new_patient = Patient.objects.create(
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                date_of_birth=form_data['dob'],
                address=form_data['address'],
                phone_number=form_data['phone_number'],
                emergency_contact_1_name=form_data['ec1_name'],
                emergency_contact_1_relationship=form_data['ec1_rel'],
                emergency_contact_1_phone=form_data['ec1_phone'],
                emergency_contact_2_name=form_data['ec2_name'],
                emergency_contact_2_relationship=form_data['ec2_rel'],
                emergency_contact_2_phone=form_data['ec2_phone'],
                reason_for_visit=form_data['visit_reason'],
                allergies=form_data['allergies'],
                current_medical_problems=form_data['medical_problems'],
                current_medications=form_data['medications'],
                insurance=form_data['insurance'] == 'True',
            )
            messages.success(request, 'Patient information submitted successfully!')
            return redirect('dashboard')

        except Exception as e:
            messages.error(request, f'Failed to save patient data: {e}')
            return render(request, 'new_patient.html', {'form_data': form_data})

    else:
        return render(request, 'new_patient.html')

class UserRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        role = self.request.POST['role']
        profile = Profile.objects.create(user=user, role=role)

        if role in ('DOC', 'ADM', 'BIL', 'NUR'):
          user.is_staff = True
          user.save()

        login(self.request, user)
        return redirect(self.success_url)

def doctor_dashboard(request):
    if request.user.is_authenticated and request.user.profile.role == 'DOC':
      open_cases = PatientCheckIn.objects.filter(doctor=request.user, status='Open')
      form = DoctorPatientInfoForm(request.POST or None)

    selected_case = None
    if request.method == 'POST':
        case_id = request.POST.get('patientCase')
        if case_id:
            selected_case = get_object_or_404(PatientCheckIn, id=case_id)
            if form.is_valid():
                info = form.save(commit=False)
                info.patient_check_in = selected_case
                info.save()
                return redirect('doctor_dashboard')

    context = {
        'open_cases': open_cases,
        'form': form,
        'selected_case': selected_case
    }
    return render(request, 'doctor_dashboard.html', context)

def doctor_input(request, check_in_id):
    check_in = get_object_or_404(PatientCheckIn, pk=check_in_id, doctor=request.user)

    try:
        info = DoctorPatientInfo.objects.get(patient_check_in=check_in)
        form = DoctorPatientInfoForm(instance=info)
    except DoctorPatientInfo.DoesNotExist:
        form = DoctorPatientInfoForm()

    if request.method == 'POST':
        form = DoctorPatientInfoForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.patient_check_in = check_in
            info.save()
            return redirect('doctor_dashboard')

    return render(request, 'doctor_form.html', {'form': form, 'check_in': check_in})

def nurse_dashboard(request):
    open_cases = PatientCheckIn.objects.filter(nurse=request.user, status='Open')
    form = NursePatientInfoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            nurse_info = form.save(commit=False)
            nurse_info.patient_check_in = PatientCheckIn.objects.get(id=request.POST.get('patient_check_in_id'))
            nurse_info.save()
            messages.success(request, "Nurse information updated successfully.")
            return redirect('nurse_dashboard')
        else:
            messages.error(request, "Error processing your form.")

    context = {
        'open_cases': open_cases,
        'form': form
    }
    return render(request, 'nurse_dashboard.html', context)

def admitting_staff_dashboard(request):
    open_cases = PatientCheckIn.objects.filter(status='Open')
    nurses = Nurse.objects.filter(user__profile__role='NUR')
    doctors = Doctor.objects.filter(user__profile__role='DOC')

    if request.method == 'POST':
        check_in_form = PatientCheckInForm(request.POST)
        if check_in_form.is_valid():
            check_in = check_in_form.save(commit=False)
            check_in.status = 'Open'
            check_in.save()
            return redirect('admitting_dashboard')
    else:
        check_in_form = PatientCheckInForm()

    context = {
        'open_cases': open_cases,
        'nurses': nurses,
        'doctors': doctors,
        'check_in_form': check_in_form
    }
    return render(request, 'admitting_dashboard.html', context)

def patient_checkin(request):
    if request.method == 'POST':
        form = PatientCheckInForm(request.POST)
        if form.is_valid():
            check_in = form.save(commit=False)
            check_in.status = 'Open'
            check_in.save()
            return redirect('admitting_dashboard')

def billing_staff_dashboard(request):
    return render(request, 'billing_dashboard.html')

def get_dashboard_url(user):
    profile = user.profile
    if profile.role == 'DOC':
        return reverse('doctor_dashboard')
    elif profile.role == 'NUR':
        return reverse('nurse_dashboard')
    elif profile.role == 'ADM':
        return reverse('admitting_dashboard')
    elif profile.role == 'BIL':
        return reverse('billing_dashboard')
    else:
        return reverse('default')

def dashboard(request):
    if request.user.is_authenticated:
        dashboard_url = get_dashboard_url(request.user)
        return redirect(dashboard_url)
    else:
        return redirect('login')

def default(request):
    error_message = request.GET.get('error_message')
    context = {'error_message': error_message}
    return render(request, 'default.html', context)

def patient_case_select_view(request):
    open_cases = PatientCheckIn.objects.filter(status='Open')
    context = {'open_cases': open_cases}
    return render(request, 'patient_case_select.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user, role=form.cleaned_data['role'])
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
