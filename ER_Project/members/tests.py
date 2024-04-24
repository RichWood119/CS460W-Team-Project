import datetime
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase, Client
from members.models import User, Patient, Profile, Doctor, Nurse, AdmittingStaff, BillingStaff, PatientCheckIn

class PatientModelTests(TestCase):

    def test_saving_valid_patient(self):
        valid_data = {
            'first_name': 'Lane',
            'last_name': 'Smith',
            'date_of_birth': '1990-01-01',
            'address': '123 Main Street',
            'phone_number': '1234567890',
            'emergency_contact_1_name': 'John Smith',
            'emergency_contact_1_relationship': 'Parent',
            'emergency_contact_1_phone': '9876543210',
            'emergency_contact_2_name': 'Mary Smith',
            'emergency_contact_2_relationship': 'Parent',
            'emergency_contact_2_phone': '9876555510',
            'reason_for_visit': 'Stomach pain',
            'insurance': True
        }
        patient = Patient(**valid_data)
        patient.save()

        self.assertIsNotNone(patient.patientID)
        self.assertEqual(patient.first_name, 'Lane')

def test_saving_invalid_phone_number(self):
    invalid_data = {
        'phone_number': 'abc123def'
    }
    patient = Patient(**invalid_data)

    with self.assertRaises(ValueError):
        patient.save()

def test_missing_required_field(self):
    data = {
        'first_name': 'Mel',
    }
    patient = Patient(**data)

    with self.assertRaises(IntegrityError):
        patient.save()

class DoctorOneToOneAndCascadeTest(TestCase):

    def test_one_to_one_relationship(self):
        user = User.objects.create_user(username='testdoc', role='DOC',  password='testpass')
        Doctor.objects.create(user=user)  # first profile creation succeeds

        with self.assertRaises(IntegrityError):
            Doctor.objects.create(user=user)  # second creation should fail

    def test_cascading_delete(self):
        user = User.objects.create_user(username='testdoc2', role='DOC',  password='testpass')
        doctor = Doctor.objects.create(user=user)

        user.delete()
        # assertion that both the doctor profile and linked objects are deleted
        self.assertFalse(Doctor.objects.filter(pk=doctor.pk).exists())

class NurseOneToOneAndCascadeTest(TestCase):

    def test_one_to_one_relationship(self):
        user = User.objects.create_user(username='testnurse', role='NUR',  password='testpass')
        Nurse.objects.create(user=user)

        with self.assertRaises(IntegrityError):
            Nurse.objects.create(user=user)

    def test_cascading_delete(self):
        user = User.objects.create_user(username='testnurse2', role='NUR',  password='testpass')
        nurse = Nurse.objects.create(user=user)

        user.delete()

        self.assertFalse(Nurse.objects.filter(pk=nurse.pk).exists())

class AdmittingStaffOneToOneAndCascadeTest(TestCase):

    def test_one_to_one_relationship(self):
        user = User.objects.create_user(username='testadmit', role='ADM',  password='testpass')
        AdmittingStaff.objects.create(user=user)

        with self.assertRaises(IntegrityError):
            AdmittingStaff.objects.create(user=user)

    def test_cascading_delete(self):
        user = User.objects.create_user(username='testadmit2', role='ADM',  password='testpass')
        admitting_staff = AdmittingStaff.objects.create(user=user)

        user.delete()

        self.assertFalse(AdmittingStaff.objects.filter(pk=admitting_staff.pk).exists())

class BillingStaffOneToOneAndCascadeTest(TestCase):

    def test_one_to_one_relationship(self):
        user = User.objects.create_user(username='testbill', role='BIL',  password='testpass')
        BillingStaff.objects.create(user=user)

        with self.assertRaises(IntegrityError):
            BillingStaff.objects.create(user=user)

    def test_cascading_delete(self):
        user = User.objects.create_user(username='testbill2', role='BIL',  password='testpass')
        billing_staff = BillingStaff.objects.create(user=user)

        user.delete()

        self.assertFalse(BillingStaff.objects.filter(pk=billing_staff.pk).exists())

class PatientCheckInModelTest(TestCase):

    def setUp(self):  # create reusable test data
      self.patient = Patient.objects.create(
          first_name='Lita',
          last_name='Smith',
          date_of_birth='1990-01-01',
          address='123 Main Street',
          phone_number='1234567890',
          emergency_contact_1_name='John Smith',
          emergency_contact_1_relationship='Parent',
          emergency_contact_1_phone='9876543210',
          emergency_contact_2_name='Mary Smith',
          emergency_contact_2_relationship='Parent',
          emergency_contact_2_phone='9876555510',
          reason_for_visit='Stomach pain',
          insurance=True
      )
      self.doctor_user = User.objects.create_user(username='testdoc', role='DOC', password='testpass')
      self.doctor = Doctor.objects.create(user=self.doctor_user)

      self.nurse_user = User.objects.create_user(username='testnurse', role='NUR', password='testpass')
      self.nurse = Nurse.objects.create(user=self.nurse_user)

    def test_valid_creation(self):
      check_in_data = {
          'patient': self.patient,
          'doctor': self.doctor_user,
          'nurse': self.nurse_user,
          'date_time': datetime.datetime.now(datetime.timezone.utc)
      }
      check_in = PatientCheckIn.objects.create(**check_in_data)
      self.assertIsNotNone(check_in.pk)

    def test_update(self):
      check_in = PatientCheckIn.objects.create(
          patient=self.patient,
          doctor=self.doctor_user,
          nurse=self.nurse_user,
          date_time=datetime.datetime.now(datetime.timezone.utc)
      )
      check_in.status = 'Closed'
      check_in.save()

      retrieved_check_in = PatientCheckIn.objects.get(pk=check_in.pk)
      self.assertEqual(retrieved_check_in.status, 'Closed')

    def test_foreign_key_deletion(self):
      check_in = PatientCheckIn.objects.create(
          patient=self.patient,
          doctor=self.doctor_user,
          nurse=self.nurse_user,
          date_time=datetime.datetime.now(datetime.timezone.utc)
      )
      self.patient.delete()
      self.assertFalse(PatientCheckIn.objects.filter(pk=check_in.pk).exists())  # Cascade delete

#View Tests (functionality/role-based access)
class LoginViewTests(TestCase):

    def setUp(self):
        self.client = Client()  # browser simulation
        self.doctor_user = User.objects.create_user(username='testdoc', role='DOC', password='test1234')
        self.doctor_user.profile.save()

class DashboardRedirectTests(TestCase):
    def setUp(self):
        self.doctor_user = User.objects.create_user(username='testdoc', role='DOC', password='test1234')
        self.client.login(username='testdoc', password='test1234')

#Template Tests (rendering)
class NavigationTests(TestCase):
    def setUp(self):
        self.doctor_user = User.objects.create_user(username='testdoc', role='DOC', password='test1234')
        Profile.objects.create(user=self.doctor_user)  # create the associated profile
