from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']

# form eto para ma change update yung user profile mo
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'firstname', 'lastname', 'location', 'address']

class ColorPreferenceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['color']

class FontPreferenceForm(forms.ModelForm):
    FONT_CHOICES = (
        ('Font1', 'Young Serif'),
        ('Font2', 'Robotto Slab'),
        ('Font3', 'Font 3'),
    )

    # Add the font field with choices
    font_preference = forms.ChoiceField(
        choices=FONT_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = Profile
        fields = ['font_preference']