import json
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

class ProfileQuizStep1Form(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label='Tell us about yourself')
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Where are you located?')
    career_interests = forms.ChoiceField(choices=[
        ('technology', 'Technology'),
        ('arts', 'Arts'),
        ('science', 'Science'),
        ('business', 'Business'),
        ('music', 'Music'),
        ('sports', 'Sports'),
        # Add more career fields as needed
    ], widget=forms.Select(attrs={'class': 'form-control'}), label='Select your career interest')

    class Meta:
        model = Profile
        fields = ['bio', 'location', 'career_interests']

import json
from django import forms
from .models import Profile

class ProfileQuizStep2Form(forms.ModelForm):
    technology_skills = [
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('javascript', 'JavaScript'),
        ('python', 'Python'),
        ('django', 'Django'),
    ]
    # Define other skill lists similarly
    business_skills = [
        ('management', 'Management'),
        ('marketing', 'Marketing'),
        ('finance', 'Finance'),
        ('sales', 'Sales'),
    ]

    career_interests = forms.CharField(widget=forms.HiddenInput(), required=False)
    skills = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[],
        label='Select your skills'
    )
    career_goals = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label='What are your career goals?')

    class Meta:
        model = Profile
        fields = ['skills', 'career_goals']

    def __init__(self, *args, **kwargs):
        super(ProfileQuizStep2Form, self).__init__(*args, **kwargs)
        career_interest = self.initial.get('career_interests', 'technology')
        if career_interest == 'technology':
            self.fields['skills'].choices = self.technology_skills
        elif career_interest == 'arts':
            self.fields['skills'].choices = self.arts_skills
        elif career_interest == 'music':
            self.fields['skills'].choices = self.music_skills
        elif career_interest == 'business':
            self.fields['skills'].choices = self.business_skills

    def save(self, commit=True):
        profile = super(ProfileQuizStep2Form, self).save(commit=False)
        skill_assessment = {
            'labels': [choice[1] for choice in self.fields['skills'].choices],
            'data': [1 for _ in self.fields['skills'].choices]
        }
        profile.skill_assessment = json.dumps(skill_assessment)
        if commit:
            profile.save()
        return profile

class ProfileQuizStep3Form(forms.ModelForm):
    resume_job_title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Job Title You Are Applying For',
        required=False
    )
    resume_skills_experiences = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Skills and Experiences',
        required=False
    )
    resume_education = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Educational Background',
        required=False
    )
    professional_experience = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Professional Experience',
        required=False
    )

    class Meta:
        model = Profile
        fields = ['resume_job_title', 'resume_skills_experiences', 'resume_education', 'professional_experience']

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
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input w-full'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input w-full'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input w-full'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input w-full'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-full'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input w-full'})   
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input w-full'})   
    )
