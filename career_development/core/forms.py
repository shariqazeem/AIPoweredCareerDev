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

    profile_picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    remove_profile_picture = forms.BooleanField(required=False, label='Remove profile picture')

    class Meta:
        model = Profile
        fields = [
            'bio', 'location', 'skills', 'career_goals', 'professional_experience', 
            'resume_job_title', 'resume_education', 'resume_skills_experiences', 'certifications_awards',
            'html_skill_level', 'css_skill_level', 'js_skill_level', 'python_skill_level', 'django_skill_level',
            'management_skill_level', 'marketing_skill_level', 'finance_skill_level', 'sales_skill_level',
            'drawing_skill_level', 'painting_skill_level', 'sculpting_skill_level', 'photography_skill_level',
            'singing_skill_level', 'instrumental_skill_level', 'composing_skill_level', 'conducting_skill_level',
            'playing_skill_level', 'coaching_skill_level', 'refereeing_skill_level', 'physical_training_skill_level',
            'profile_picture'
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['html_skill_level'].initial = self.instance.html_skill_level
        self.fields['css_skill_level'].initial = self.instance.css_skill_level
        self.fields['js_skill_level'].initial = self.instance.js_skill_level
        self.fields['python_skill_level'].initial = self.instance.python_skill_level
        self.fields['django_skill_level'].initial = self.instance.django_skill_level
        
        self.fields['management_skill_level'].initial = self.instance.management_skill_level
        self.fields['marketing_skill_level'].initial = self.instance.marketing_skill_level
        self.fields['finance_skill_level'].initial = self.instance.finance_skill_level
        self.fields['sales_skill_level'].initial = self.instance.sales_skill_level
        
        self.fields['drawing_skill_level'].initial = self.instance.drawing_skill_level
        self.fields['painting_skill_level'].initial = self.instance.painting_skill_level
        self.fields['sculpting_skill_level'].initial = self.instance.sculpting_skill_level
        self.fields['photography_skill_level'].initial = self.instance.photography_skill_level
        
        self.fields['singing_skill_level'].initial = self.instance.singing_skill_level
        self.fields['instrumental_skill_level'].initial = self.instance.instrumental_skill_level
        self.fields['composing_skill_level'].initial = self.instance.composing_skill_level
        self.fields['conducting_skill_level'].initial = self.instance.conducting_skill_level
        
        self.fields['playing_skill_level'].initial = self.instance.playing_skill_level
        self.fields['coaching_skill_level'].initial = self.instance.coaching_skill_level
        self.fields['refereeing_skill_level'].initial = self.instance.refereeing_skill_level
        self.fields['physical_training_skill_level'].initial = self.instance.physical_training_skill_level

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        
        skill_assessment = {
            'labels': [],
            'data': []
        }
        if self.cleaned_data.get('remove_profile_picture'):
            profile.profile_picture.delete(save=False)
            profile.profile_picture = None
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
    bio_choices = [
        ('student', 'I am a student'),
        ('professional', 'I am a professional'),
        ('career_change', 'I am looking to change my career'),
    ]
    bio = forms.ChoiceField(choices=bio_choices, widget=forms.Select(attrs={'class': 'form-control'}), label='Tell us about yourself')
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your location'}), label='Where are you located?')
    career_interests = forms.ChoiceField(choices=[
        ('technology', 'Technology'),
        ('arts', 'Arts'),
        ('science', 'Science'),
        ('business', 'Business'),
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('fashion', 'Fashion Designing'),
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
        ('nodejs', 'Node.js'),
        ('php', 'PHP'),
        ('java', 'Java'),
        ('csharp', 'C#'),
        ('cpp', 'C++'),
        ('sql', 'SQL'),
        ('react', 'React'),
        ('angular', 'Angular'),
    ]
    business_skills = [
        ('management', 'Management'),
        ('marketing', 'Marketing'),
        ('finance', 'Finance'),
        ('sales', 'Sales'),
        ('accounting', 'Accounting'),
        ('hr', 'Human Resources'),
        ('operations', 'Operations'),
        ('strategic_planning', 'Strategic Planning'),
    ]
    arts_skills = [
        ('drawing', 'Drawing'),
        ('painting', 'Painting'),
        ('sculpting', 'Sculpting'),
        ('photography', 'Photography'),
        ('graphic_design', 'Graphic Design'),
        ('illustration', 'Illustration'),
        ('animation', 'Animation'),
        ('printmaking', 'Printmaking'),
    ]
    music_skills = [
        ('instrument_playing', 'Instrument Playing'),
        ('vocals', 'Vocals'),
        ('composition', 'Composition'),
        ('music_production', 'Music Production'),
        ('music_theory', 'Music Theory'),
        ('conducting', 'Conducting'),
        ('djing', 'DJing'),
        ('sound_engineering', 'Sound Engineering'),
    ]
    sports_skills = [
        ('team_sports', 'Team Sports'),
        ('individual_sports', 'Individual Sports'),
        ('coaching', 'Coaching'),
        ('fitness', 'Fitness'),
        ('nutrition', 'Nutrition'),
        ('physiotherapy', 'Physiotherapy'),
        ('sports_management', 'Sports Management'),
    ]
    fashion_skills = [
        ('fashion_designing', 'Fashion Designing'),
        ('fashion_styling', 'Fashion Styling'),
        ('fashion_illustration', 'Fashion Illustration'),
        ('fashion_merchandising', 'Fashion Merchandising'),
        ('textile_design', 'Textile Design'),
        ('pattern_making', 'Pattern Making'),
        ('sewing', 'Sewing'),
        ('fashion_marketing', 'Fashion Marketing'),
    ]

    career_interests = forms.CharField(widget=forms.HiddenInput(), required=False)
    skills = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[],
        label='Select your skills'
    )
    other_skills = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, label='Other Skills')
    career_goals = forms.ChoiceField(
        choices=[
            ('leader', 'Become a Leader in my Field'),
            ('specialist', 'Become a Specialist in my Area'),
            ('management', 'Move into Management'),
            ('business', 'Start my Own Business'),
            ('skills', 'Develop New Skills'),
            ('network', 'Expand my Professional Network'),
            ('balance', 'Achieve a Better Work-Life Balance'),
            ('recognition', 'Gain Recognition in my Industry'),
            ('innovation', 'Drive Innovation and Change'),
        ],
        widget=forms.RadioSelect,
        label='Select your career goals'
    )

    class Meta:
        model = Profile
        fields = ['skills', 'other_skills', 'career_goals']

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
        elif career_interest == 'fashion':
            self.fields['skills'].choices = self.fashion_skills

    def save(self, commit=True):
        profile = super(ProfileQuizStep2Form, self).save(commit=False)
        profile.skills = ','.join(self.cleaned_data['skills'])
        if commit:
            profile.save()
        return profile



class ProfileQuizStep3Form(forms.ModelForm):
    resume_job_title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title (optional)'}),
        label='Job Title You Are Applying For (if any)',
        required=False
    )
    resume_skills_experiences = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your skills and experiences'}),
        label='Skills and Experiences',
        required=True
    )
    resume_education = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your educational background'}),
        label='Educational Background',
        required=True
    )
    professional_experience = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your professional experience'}),
        label='Professional Experience',
        required=True
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

    career_interests = forms.CharField(widget=forms.HiddenInput(), required=False)

    all_fields = {
        'html': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='HTML Skill Level', required=False),
        'css': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='CSS Skill Level', required=False),
        'javascript': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='JavaScript Skill Level', required=False),
        'python': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Python Skill Level', required=False),
        'django': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Django Skill Level', required=False),
        'nodejs': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Node.js Skill Level', required=False),
        'php': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='PHP Skill Level', required=False),
        'java': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Java Skill Level', required=False),
        'csharp': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='C# Skill Level', required=False),
        'cpp': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='C++ Skill Level', required=False),
        'sql': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='SQL Skill Level', required=False),
        'react': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='React Skill Level', required=False),
        'angular': forms.ChoiceField(choices=skill_levels, widget=forms.Select(attrs={'class': 'form-control'}), label='Angular Skill Level', required=False),
        # Add more skill fields as needed
    }

    class Meta:
        model = Profile
        fields = []

    def __init__(self, *args, **kwargs):
        super(ProfileQuizStep4Form, self).__init__(*args, **kwargs)
        career_interest = self.initial.get('career_interests', 'technology')
        selected_skills = self.initial.get('selected_skills', '').split(',')

        for skill in selected_skills:
            if skill in self.all_fields:
                self.fields[f'{skill}_skill_level'] = self.all_fields[skill]

    def save(self, commit=True):
        profile = super(ProfileQuizStep4Form, self).save(commit=False)
        skill_assessment = {
            'labels': [],
            'data': []
        }
        for field in self.fields:
            if field.endswith('_skill_level'):
                skill_assessment['labels'].append(self.fields[field].label)
                skill_assessment['data'].append(int(self.cleaned_data.get(field, 0)))
        profile.skill_assessment = json.dumps(skill_assessment)
        if commit:
            profile.save()
        return profile


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

class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['private']
        widgets = {
            'private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DeleteAccountForm(forms.Form):
    confirm = forms.CharField(max_length=50, label="Type 'DELETE' to confirm")
