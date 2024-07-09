from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
import json

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    skill_levels = [
        ('1', 'Beginner'),
        ('2', 'Intermediate'),
        ('3', 'Advanced'),
    ]

    html_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='HTML Skill Level', required=False)
    css_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='CSS Skill Level', required=False)
    js_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='JavaScript Skill Level', required=False)
    python_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Python Skill Level', required=False)
    django_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Django Skill Level', required=False)
    
    management_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Management Skill Level', required=False)
    marketing_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Marketing Skill Level', required=False)
    finance_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Finance Skill Level', required=False)
    sales_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Sales Skill Level', required=False)
    
    drawing_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Drawing Skill Level', required=False)
    painting_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Painting Skill Level', required=False)
    sculpting_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Sculpting Skill Level', required=False)
    photography_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Photography Skill Level', required=False)
    
    singing_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Singing Skill Level', required=False)
    instrumental_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Instrumental Skill Level', required=False)
    composing_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Composing Skill Level', required=False)
    conducting_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Conducting Skill Level', required=False)
    
    playing_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Playing Skill Level', required=False)
    coaching_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Coaching Skill Level', required=False)
    refereeing_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Refereeing Skill Level', required=False)
    physical_training_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Physical Training Skill Level', required=False)

    class Meta:
        model = Profile
        fields = [
            'bio', 'location', 'skills', 'career_goals', 'professional_experience', 
            'resume_job_title', 'resume_education', 'resume_skills_experiences', 'certifications_awards',
            'html_skill_level', 'css_skill_level', 'js_skill_level', 'python_skill_level', 'django_skill_level',
            'management_skill_level', 'marketing_skill_level', 'finance_skill_level', 'sales_skill_level',
            'drawing_skill_level', 'painting_skill_level', 'sculpting_skill_level', 'photography_skill_level',
            'singing_skill_level', 'instrumental_skill_level', 'composing_skill_level', 'conducting_skill_level',
            'playing_skill_level', 'coaching_skill_level', 'refereeing_skill_level', 'physical_training_skill_level'
        ]

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        
        skill_assessment = {
            'labels': [],
            'data': []
        }
        
        career_interests = profile.career_interests
        skill_fields = []
        
        if career_interests == 'technology':
            skill_fields = ['html_skill_level', 'css_skill_level', 'js_skill_level', 'python_skill_level', 'django_skill_level']
        elif career_interests == 'business':
            skill_fields = ['management_skill_level', 'marketing_skill_level', 'finance_skill_level', 'sales_skill_level']
        elif career_interests == 'arts':
            skill_fields = ['drawing_skill_level', 'painting_skill_level', 'sculpting_skill_level', 'photography_skill_level']
        elif career_interests == 'music':
            skill_fields = ['singing_skill_level', 'instrumental_skill_level', 'composing_skill_level', 'conducting_skill_level']
        elif career_interests == 'sports':
            skill_fields = ['playing_skill_level', 'coaching_skill_level', 'refereeing_skill_level', 'physical_training_skill_level']
        
        for field in skill_fields:
            skill_assessment['labels'].append(self.fields[field].label)
            skill_assessment['data'].append(int(self.cleaned_data.get(field, 0)))

        profile.skill_assessment = json.dumps(skill_assessment)
        if commit:
            profile.save()
        return profile

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



class ProfileQuizStep2Form(forms.ModelForm):
    technology_skills = [
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('javascript', 'JavaScript'),
        ('python', 'Python'),
        ('django', 'Django'),
    ]
    business_skills = [
        ('management', 'Management'),
        ('marketing', 'Marketing'),
        ('finance', 'Finance'),
        ('sales', 'Sales'),
    ]
    arts_skills = [
        ('drawing', 'Drawing'),
        ('painting', 'Painting'),
        ('sculpting', 'Sculpting'),
        ('photography', 'Photography'),
    ]
    music_skills = [
        ('instrument', 'Instrument Playing'),
        ('vocals', 'Vocals'),
        ('composition', 'Composition'),
        ('production', 'Music Production'),
    ]
    sports_skills = [
        ('team_sports', 'Team Sports'),
        ('individual_sports', 'Individual Sports'),
        ('coaching', 'Coaching'),
        ('fitness', 'Fitness'),
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
        elif career_interest == 'sports':
            self.fields['skills'].choices = self.sports_skills

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


class ProfileQuizStep4Form(forms.ModelForm):
    skill_levels = [
        ('1', 'Beginner'),
        ('2', 'Intermediate'),
        ('3', 'Advanced'),
    ]

    html_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='HTML Skill Level', required=False)
    css_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='CSS Skill Level', required=False)
    js_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='JavaScript Skill Level', required=False)
    python_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Python Skill Level', required=False)
    django_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Django Skill Level', required=False)

    management_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Management Skill Level', required=False)
    marketing_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Marketing Skill Level', required=False)
    finance_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Finance Skill Level', required=False)
    sales_skill_level = forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Sales Skill Level', required=False)

    class Meta:
        model = Profile
        fields = [
            'html_skill_level', 'css_skill_level', 'js_skill_level', 'python_skill_level', 'django_skill_level',
            'management_skill_level', 'marketing_skill_level', 'finance_skill_level', 'sales_skill_level'
        ]

    def save(self, commit=True):
        profile = super(ProfileQuizStep4Form, self).save(commit=False)
        skill_assessment = {
            'labels': ['HTML', 'CSS', 'JavaScript', 'Python', 'Django', 'Management', 'Marketing', 'Finance', 'Sales'],
            'data': [
                int(self.cleaned_data.get('html_skill_level', 0)),
                int(self.cleaned_data.get('css_skill_level', 0)),
                int(self.cleaned_data.get('js_skill_level', 0)),
                int(self.cleaned_data.get('python_skill_level', 0)),
                int(self.cleaned_data.get('django_skill_level', 0)),
                int(self.cleaned_data.get('management_skill_level', 0)),
                int(self.cleaned_data.get('marketing_skill_level', 0)),
                int(self.cleaned_data.get('finance_skill_level', 0)),
                int(self.cleaned_data.get('sales_skill_level', 0))
            ]
        }
        profile.skill_assessment = json.dumps(skill_assessment)
        if commit:
            profile.save()
        return profile


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
