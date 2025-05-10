from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'phone_number', 'institute', 'facebook_link',
            'discord_username', 'vjudge_username',
            'codeforces_username', 'total_unique_solves',
            'codeforces_max_rating',
        ]
