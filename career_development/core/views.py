from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.http import JsonResponse
from .forms import UserUpdateForm, ProfileUpdateForm, ProfileStep1Form, ProfileStep2Form, ProfileStep3Form, ProfileQuizStep1Form, ProfileQuizStep2Form, ProfileQuizStep3Form, CustomAuthenticationForm, CustomUserCreationForm
from .models import Resource, Connection, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as django_logout  # Rename Django's logout function to avoid conflict

import google.generativeai as genai

genai.configure(api_key=settings.GEMINI_API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Signup successful! Please check your email to activate your account.')
            return redirect('login')
        else:
            messages.error(request, 'Signup failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Login failed. Please check your username and password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully.')
        return redirect('login')
    else:
        messages.error(request, 'The activation link is invalid.')
        return render(request, 'account/activation_invalid.html')

def logout(request):
    django_logout(request)
    return redirect('login')

@login_required
def complete_profile_step1(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileQuizStep1Form(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('complete_profile_step2')
    else:
        form = ProfileQuizStep1Form(instance=profile)
    return render(request, 'account/complete_profile_step1.html', {'form': form})

@login_required
def complete_profile_step2(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileQuizStep2Form(request.POST, instance=profile, initial={'career_interests': profile.career_interests})
        if form.is_valid():
            form.save()
            return redirect('complete_profile_step3')
    else:
        form = ProfileQuizStep2Form(instance=profile, initial={'career_interests': profile.career_interests})
    return render(request, 'account/complete_profile_step2.html', {'form': form})

@login_required
def complete_profile_step3(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileQuizStep3Form(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile setup completed successfully.')
            return redirect('profile')
    else:
        form = ProfileQuizStep3Form(instance=profile)
    return render(request, 'account/complete_profile_step3.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    recommendations = request.user.profile.career_recommendations
    job_listings = request.user.profile.job_prospects

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'recommendations': recommendations,
        'job_listings': job_listings
    })

@login_required
def profile_details(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'profile_details.html', {
        'profile_form': profile_form
    })

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    recommendations = get_career_recommendations(user)
    job_postings = get_job_listings(user)
    return render(request, 'user_profile.html', {'profile_user': user, 'recommendations': recommendations, 'job_postings': job_postings})

def resources(request):
    resource_list = Resource.objects.all()
    return render(request, 'resources.html', {'resources': resource_list})

@login_required
def connect(request, username):
    user_to_connect = get_object_or_404(User, username=username)
    Connection.objects.get_or_create(user_from=request.user, user_to=user_to_connect)
    return redirect('user_profile', username=username)

@login_required
def connections(request):
    user_connections = Connection.objects.filter(user_from=request.user)
    return render(request, 'connections.html', {'connections': user_connections})

def get_career_recommendations(user):
    data = {
        "bio": user.profile.bio,
        "skills": user.profile.skills,
        "career_goals": user.profile.career_goals,
    }

    prompt = f"Generate career recommendations for a user with the following details: {data}"

    response = model.generate_content(prompt)

    if response and hasattr(response, 'text'):
        recommendations = response.text.strip().split('\n')
        recommendations_html = generate_html_from_text(recommendations)
        return recommendations_html
    else:
        return "<p>No recommendations available.</p>"

def get_job_listings(user):
    profile = get_object_or_404(Profile, user=user)
    
    data = {
        "skills": profile.skills,
        "location": profile.location,
        "career_goals": profile.career_goals,
    }

    prompt = f"Generate job listings for a user with the following details: {data}"

    response = model.generate_content(prompt)

    if response and hasattr(response, 'text'):
        job_listings = response.text.strip().split('\n')
        job_listings_html = generate_html_from_text(job_listings)
        return job_listings_html
    else:
        return "<p>No job listings available.</p>"

def generate_html_from_text(text_list):
    html_content = ""
    in_list = False

    for line in text_list:
        line = line.strip()
        
        if line.startswith('##'):
            html_content += f"<h2>{line[2:].strip()}</h2>"
        elif line.startswith('#'):
            html_content += f"<h1>{line[1:].strip()}</h1>"
        elif line.startswith('**') and line.endswith('**'):
            html_content += f"<strong>{line[2:-2].strip()}</strong><br>"
        elif line.startswith('**') and line.endswith(':**'):
            html_content += f"<h3>{line[2:-3].strip()}</h3>"
        elif line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. '):
            if in_list:
                html_content += "</li>"
            else:
                in_list = True
                html_content += "<ol><li>"
            html_content += line.strip()[3:] + "</li><li>"
        elif line.startswith('* '):
            if not in_list:
                html_content += "<ul>"
                in_list = True
            html_content += f"<li>{line[2:].strip()}</li>"
        else:
            if in_list:
                html_content += "</ul>" if in_list else "</ol>"
                in_list = False
            html_content += f"<p>{line}</p>"

    if in_list:
        html_content += "</ul>" if in_list else "</ol>"

    return html_content

@login_required
def career_recommendations(request):
    recommendations = get_career_recommendations(request.user)
    return render(request, 'career_recommendations.html', {'recommendations': recommendations})

@login_required
def job_prospects(request):
    job_listings = get_job_listings(request.user)
    return render(request, 'job_prospects.html', {'job_listings': job_listings})

@login_required
def dashboard(request):
    profile = request.user.profile

    context = {
        'user': request.user,
        'profile': profile,
        'skill_assessment': profile.skill_assessment,
        'resume_advice': profile.resume_advice,
        'matched_jobs': profile.matched_jobs,
        'learning_resources': profile.learning_resources,
        'networking_opportunities': profile.networking_opportunities,
        'career_recommendations': profile.career_recommendations,
        'job_prospects': profile.job_prospects,
    }
    return render(request, 'dashboard.html', context)

@login_required
def get_career_recommendations(request):
    profile = request.user.profile
    response = model.generate_content(f"Generate career recommendations for a user with the following details: {profile.bio}, {profile.skills}, {profile.career_goals}")

    if response and hasattr(response, 'text'):
        profile.career_recommendations = response.text
        profile.save()
        return JsonResponse({'status': 'success', 'career_recommendations': profile.career_recommendations})

    return JsonResponse({'status': 'error', 'message': 'Failed to generate career recommendations.'}, status=400)

@login_required
def get_job_prospects(request):
    profile = request.user.profile
    response = model.generate_content(f"Generate job prospects for a user with the following details: {profile.skills}, {profile.location}, {profile.career_goals}")

    if response and hasattr(response, 'text'):
        profile.job_prospects = response.text
        profile.save()
        return JsonResponse({'status': 'success', 'job_prospects': profile.job_prospects})

    return JsonResponse({'status': 'error', 'message': 'Failed to generate job prospects.'}, status=400)

@login_required
def assess_skills(request):
    profile = request.user.profile
    response = model.generate_content(f"Assess the following skills: {profile.skills}")

    if response and hasattr(response, 'text'):
        profile.skill_assessment = response.text
        profile.save()
        return JsonResponse({'status': 'success', 'skill_assessment': profile.skill_assessment})

    return JsonResponse({'status': 'error', 'message': 'Failed to assess skills.'}, status=400)

@login_required
def get_resume_advice(request):
    profile = request.user.profile
    response = model.generate_content(f"Give resume advice for the following text: {profile.professional_experience}")

    if response and hasattr(response, 'text'):
        profile.resume_advice = response.text
        profile.save()
        return JsonResponse({'status': 'success', 'resume_advice': profile.resume_advice})

    return JsonResponse({'status': 'error', 'message': 'Failed to generate resume advice.'}, status=400)

@login_required
def match_jobs(request):
    profile = request.user.profile
    user_data = {
        'skills': profile.skills,
        'location': profile.location,
        'career_goals': profile.career_goals
    }
    response = model.generate_content(f"Match jobs for a user with the following details: {user_data}")

    if response and hasattr(response, 'text'):
        profile.matched_jobs = response.text
        profile.save()
        return JsonResponse({'status': 'success', 'matched_jobs': profile.matched_jobs})

    return JsonResponse({'status': 'error', 'message': 'Failed to match jobs.'}, status=400)

@login_required
def get_learning_resources(request):
    profile = request.user.profile
    response = model.generate_content(f"Provide learning resources for the following skills: {profile.skills}")

    if response and hasattr(response, 'text'):
        profile.learning_resources = response.text
        profile.save()
        return JsonResponse({'status': 'success', 'learning_resources': profile.learning_resources})

    return JsonResponse({'status': 'error', 'message': 'Failed to fetch learning resources.'}, status=400)

@login_required
def find_networking_opportunities(request):
    profile = request.user.profile
    response = model.generate_content(f"Find networking opportunities for the following interests: {profile.career_goals}")

    if response and hasattr(response, 'text'):
        profile.networking_opportunities = response.text
        profile.save()
        return JsonResponse({'status': 'success', 'networking_opportunities': profile.networking_opportunities})

    return JsonResponse({'status': 'error', 'message': 'Failed to fetch networking opportunities.'}, status=400)


import json

@login_required
def dash(request):
    profile = request.user.profile

    if not profile.is_complete:
        return redirect('complete_profile_step1')

    career_progress = profile.career_progress if profile.career_progress else {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June'],
        'data': [0, 10, 5, 2, 20, 30]
    }

    skill_assessment = profile.skill_assessment if profile.skill_assessment else {
        'labels': ['HTML', 'CSS', 'JavaScript', 'Python', 'Django'],
        'data': [0, 0, 0, 0, 0]
    }

    context = {
        'career_progress': json.dumps(career_progress),
        'skill_assessment': json.dumps(skill_assessment),
    }

    return render(request, 'dash.html', context)
