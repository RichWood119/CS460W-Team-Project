from django.urls import path
from . import views
from .views import UserRegistrationView

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
    path('dashboard/admitting/', views.admitting_staff_dashboard, name='admitting_staff_dashboard'),
    path('dashboard/billing/', views.billing_staff_dashboard, name='billing_staff_dashboard'),
]
