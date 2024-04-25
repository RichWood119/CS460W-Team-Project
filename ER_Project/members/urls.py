from django.urls import path
from . import views
from .views import UserRegistrationView
from .views import patient_checkin, doctor_input

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('patients/', views.patient_list, name='patient_list'),
    path('new_patient/', views.new_patient, name='new_patient'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/nurse/', views.nurse_dashboard, name='nurse_dashboard'),
    path('dashboard/admitting/', views.admitting_staff_dashboard, name='admitting_dashboard'),
    path('dashboard/admitting/checkin/', patient_checkin, name='patient_checkin'),
    path('dashboard/doctor/input/<int:check_in_id>/', views.doctor_input, name='doctor_input'),
    path('dashboard/doctor/form/<int:case_id>/', views.doctor_form, name='doctor_form'),
    path('dashboard/nurse/input/<int:check_in_id>/', views.nurse_input, name='nurse_input'),
    path('case/edit/<int:case_id>/', views.edit_case, name='edit_case'),
    path('dashboard/nurse/form/<int:case_id>/', views.nurse_form, name='nurse_form'),
    path('dashboard/billing/', views.billing_staff_dashboard, name='billing_dashboard'),
    path('default/', views.default, name='default'),
]
