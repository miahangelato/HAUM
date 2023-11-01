from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


#This code defines a signal handler function named create_profile that automatically creates a Profile object associated with a newly created user instance when the user is created.

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     """
#     Save the profile of the user instance.
#     """
#     if hasattr(instance, 'profile'):
#         """
#         Check if the profile attribute exists before calling save on it.
#         """
#         instance.profile.save()

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()




#This code defines a signal handler function named save_profile that automatically saves the associated Profile object whenever a User object is saved.


