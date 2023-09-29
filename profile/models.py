from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
# from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'
    # display nya username profile

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# post_save.connect(create_profile, sender=User)
  # AFTER MO GUFMAWA NG MODELS LAGAY MO SA ADMINv