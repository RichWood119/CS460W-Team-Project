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
