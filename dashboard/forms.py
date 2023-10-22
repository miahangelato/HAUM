from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from profile.models import Profile


class EditUserForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = (
            # 'email',
            # 'username',
            'first_name',
            'last_name',
            # 'password',
            'bio',
            'location',
            'address',

            # 'color',
            # 'font_preference',
            # 'image',
            # 'location',
            # 'address',
            # 'bio',
            # 'image',
            # 'color',
            # 'font_preference',
        )