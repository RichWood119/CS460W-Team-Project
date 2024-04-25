from django.db.models.signals import post_save
from django.dispatch import receiver
from members.models import Doctor, Nurse, AdmittingStaff, BillingStaff, User, Profile
from .models import User, Profile

@receiver(post_save, sender=User)
def create_profile_handler(sender, instance, created, **kwargs):
    if not created:
      return
    profile = Profile(user=instance)
    profile.save()

    # Create the appropriate staff object if the role is set:
    if instance.profile.role == 'DOC':
        Doctor.objects.create(user=instance)
    elif instance.profile.role == 'NUR':
        Nurse.objects.create(user=instance)
    elif instance.profile.role == 'ADM':
        AdmittingStaff.objects.create(user=instance)
    elif instance.profile.role == 'BIL':
        BillingStaff.objects.create(user=instance)
