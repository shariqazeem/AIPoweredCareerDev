from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'skills', 'career_goals', 'professional_experience']


class ProfileStep1Form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location']

class ProfileStep2Form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['skills', 'career_goals']

class ProfileStep3Form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['professional_experience']
