from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'phone_number', 'institute', 'facebook_link',
            'discord_username', 'vjudge_username',
            'codeforces_username', 'total_unique_solves',
            'codeforces_max_rating',
        ]
        

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
        strip=False,
        help_text=False,
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        strip=False,
        help_text=False,
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        strip=False,
        help_text=False,
    )