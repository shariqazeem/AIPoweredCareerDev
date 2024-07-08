from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label = 'Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input w-full'})
    )
    password2 = forms.CharField(
        label = 'Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input w-full'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input w-full'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-full'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget= forms.TextInput(attrs={'class': 'form-input w-full'})   
    )
    password = forms.CharField(
        widget= forms.PasswordInput(attrs={'class': 'form-input w-full'})   
    )