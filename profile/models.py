from colorfield.fields import ColorField
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver


class Location(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


#GINALAW NAME
class Profile(models.Model):
    # color = models.CharField(max_length=7, blank=True, null=True)
    color = ColorField(default='#720026')
    font_preference = models.CharField(max_length=50, default='Young Serif') # Changed default font to Young Serif
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'
    # display nya username profile
    #Fixed this function, walang double underscore ung str (arnaz)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def create_profile(sender, instance, created,kwargs):
        if created:
            Profile.objects.create(user=instance)
            # post_save.connect(create_profile, sender=User)
# AFTER MO GUFMAWA NG MODELS LAGAY MO SA ADMINv


# Path: profile/admin.py
class UserVote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_upvote = models.BooleanField(default=True)

    class Meta:
        unique_together = ('voter', 'profile')