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
        fields = ['firstname', 'lastname', 'bio', 'address', 'location', 'image', 'color', 'font_preference']


#Color Preference Form can be deleted since the color field is already in the ProfileUpdateForm
class ColorPreferenceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['color']


class FontPreferenceForm(forms.ModelForm):
    FONT_CHOICES = (
        ('Young Serif', 'Young Serif'),
        ('Roboto Slab', 'Roboto Slab'),
        ('Noto Sans JP', 'Noto Sans JP'),
        ('Yuji Hentaigana Akari', 'Yuji Hentaigana Akari'),
    )
    # Replaced the font field with choices added new font option

    # Add the font field with choices
    font_preference = forms.ChoiceField(
        choices=FONT_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Profile
        fields = ['font_preference']