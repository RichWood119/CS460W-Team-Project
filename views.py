from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from .forms import RegistrationForm, PatientCheckInForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.views.generic import CreateView
from .models import Patient, Profile, PatientCheckIn

def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

def nurse_dashboard(request):
    return render(request, 'nurse_dashboard.html')

def admitting_staff_dashboard(request):
    return render(request, 'admitting_dashboard.html')

def billing_staff_dashboard(request):
    return render(request, 'billing_dashboard.html')

def get_dashboard_url(user):
    profile = user.profile
    if profile.role == 'DOC':
        return reverse('doctor_dashboard')
    elif profile.role == 'NUR':
        return reverse('nurse_dashboard')
    elif profile.role == 'ADM':
        return reverse('admitting_staff_dashboard')
    elif profile.role == 'BIL':
        return reverse('billing_staff_dashboard')
    else:
        return reverse('dashboard')

def admitting_staff_view(request):
    if request.method == 'POST':
        check_in_form = PatientCheckInForm(request.POST)
        if check_in_form.is_valid():
            check_in = check_in_form.save()
            return redirect('admitting_dashboard.html')
    else:
        check_in_form = PatientCheckInForm()
    context = {'check_in_form': check_in_form}
    return render(request, 'admitting_dashboard.html', context)
