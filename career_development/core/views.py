from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from career_development import settings as project_settings
from django.http import JsonResponse
from .forms import UserUpdateForm, ProfileUpdateForm, ProfileQuizStep1Form, ProfileQuizStep2Form, ProfileQuizStep3Form, ProfileQuizStep4Form, CustomAuthenticationForm, CustomUserCreationForm, PrivacySettingsForm, DeleteAccountForm
from .models import Resource, Connection, Profile, Message, Feedback, Badge, UserBadge
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as django_logout
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import google.generativeai as genai
from django.db.models import Q
from django.views.decorators.http import require_GET, require_POST
import pusher
from django.views.decorators.csrf import csrf_exempt
import logging
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

pusher_client = pusher.Pusher(
    app_id = "1834647",
    key = "b398130b0aca7c48575e",
    secret = "c9075fca224ef336733b",
    cluster = "mt1",
    ssl=True,
)

genai.configure(api_key=project_settings.GEMINI_API_KEY)  # Use project_settings here

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

@csrf_exempt
def google_one_tap_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get('credential')
            logger.debug(f"Received token: {token}")

            idinfo = id_token.verify_oauth2_token(token, requests.Request(), "143450501986-0bs7v2vcmeimcv5daq1e9st5vs5s1eed.apps.googleusercontent.com")
            logger.debug(f"ID Info: {idinfo}")

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                logger.error("Wrong issuer.")
                return JsonResponse({'success': False, 'error': 'Wrong issuer.'})

            email = idinfo['email']
            logger.debug(f"Email: {email}")

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create_user(username=email, email=email, password=None)
                user.save()
                logger.debug(f"Created new user: {user}")

            # Set the backend attribute before calling auth_login
            user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
            auth_login(request, user)  # Correctly pass both request and user to login()
            return JsonResponse({'success': True})

        except ValueError as e:
            logger.error(f"Token verification failed: {e}")
            return JsonResponse({'success': False, 'error': f'Token verification failed: {e}'})
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({'success': False, 'error': f'Unexpected error: {e}'})
    
    logger.error("Invalid request method.")
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

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
        initial_data = {'career_interests': profile.career_interests}
        if profile.skills:
            initial_data['skills'] = profile.skills.split(',')
        form = ProfileQuizStep2Form(instance=profile, initial=initial_data)
    return render(request, 'account/complete_profile_step2.html', {'form': form})

@login_required
def complete_profile_step3(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileQuizStep3Form(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('complete_profile_step4')
    else:
        form = ProfileQuizStep3Form(instance=profile)
    
    return render(request, 'account/complete_profile_step3.html', {'form': form})


@login_required
def complete_profile_step4(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileQuizStep4Form(request.POST, instance=profile, initial={'career_interests': profile.career_interests, 'selected_skills': profile.skills})
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile setup completed successfully.')
            award_badge(request, 'Newbie')  # Pass request object
            return redirect('dashboard')
    else:
        form = ProfileQuizStep4Form(instance=profile, initial={'career_interests': profile.career_interests, 'selected_skills': profile.skills})
    return render(request, 'account/complete_profile_step4.html', {'form': form})



@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if created:
        # Award "Newbie" badge for new profile creation
        try:
            newbie_badge = Badge.objects.get(name='Newbie')
            if not UserBadge.objects.filter(user=request.user, badge=newbie_badge).exists():
                UserBadge.objects.create(user=request.user, badge=newbie_badge)
                messages.success(request, f"Congratulations! You've earned the {newbie_badge.name} badge.")
        except Badge.DoesNotExist:
            pass  # Handle case where "Newbie" badge does not exist

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # Award badge for updating profile
            try:
                profile_updated_badge = Badge.objects.get(name='Profile Updated')
                if not UserBadge.objects.filter(user=request.user, badge=profile_updated_badge).exists():
                    UserBadge.objects.create(user=request.user, badge=profile_updated_badge)
                    messages.success(request, f"Congratulations! You've earned the {profile_updated_badge.name} badge.")
            except Badge.DoesNotExist:
                pass  # Handle case where "Profile Updated" badge does not exist

            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    recommendations = request.user.profile.career_recommendations
    job_listings = request.user.profile.job_prospects
    badges = UserBadge.objects.filter(user=request.user).select_related('badge')

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'recommendations': recommendations,
        'job_listings': job_listings,
        'badges': badges,  # Pass the badges to the template
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def change_profile_picture(request):
    profile = request.user.profile
    if 'profile_picture' in request.FILES:
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'No file uploaded'}, status=400)

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
    profile = user.profile
    is_connected = Connection.objects.filter(user_from=request.user, user_to=user).exists()

    return render(request, 'user_profile.html', {
        'profile_user': user,
        'is_private': profile.private,
        'is_connected': is_connected,
    })


def resources(request):
    resource_list = Resource.objects.all()
    return render(request, 'resources.html', {'resources': resource_list})

@login_required
def connect(request, username):
    user_to_connect = get_object_or_404(User, username=username)
    Connection.objects.get_or_create(user_from=request.user, user_to=user_to_connect)
    award_badge(request, 'Connect')  # Pass request object
    return redirect('user_profile', username=username)

@login_required
def connections(request):
    user_connections = Connection.objects.filter(user_from=request.user)
    connection_requests = ConnectionRequest.objects.filter(to_user=request.user, accepted=False)
    sent_requests = ConnectionRequest.objects.filter(from_user=request.user, accepted=False)
    return render(request, 'connections.html', {
        'connections': user_connections,
        'requests': connection_requests,
        'sent_requests': sent_requests
    })

def get_skill_assessment(profile):
    skill_assessment = {
        'labels': [],
        'data': []
    }
    if profile.career_interests == 'technology':
        skill_assessment['labels'] = ['HTML', 'CSS', 'JavaScript', 'Python', 'Django']
        skill_assessment['data'] = [
            profile.html_skill_level or 1,
            profile.css_skill_level or 1,
            profile.js_skill_level or 1,
            profile.python_skill_level or 1,
            profile.django_skill_level or 1,
        ]
    elif profile.career_interests == 'business':
        skill_assessment['labels'] = ['Management', 'Marketing', 'Finance', 'Sales']
        skill_assessment['data'] = [
            profile.management_skill_level or 1,
            profile.marketing_skill_level or 1,
            profile.finance_skill_level or 1,
            profile.sales_skill_level or 1,
        ]
    elif profile.career_interests == 'arts':
        skill_assessment['labels'] = ['Drawing', 'Painting', 'Sculpting', 'Photography']
        skill_assessment['data'] = [
            profile.drawing_skill_level or 1,
            profile.painting_skill_level or 1,
            profile.sculpting_skill_level or 1,
            profile.photography_skill_level or 1,
        ]
    elif profile.career_interests == 'music':
        skill_assessment['labels'] = ['Singing', 'Instrumental', 'Composing', 'Conducting']
        skill_assessment['data'] = [
            profile.singing_skill_level or 1,
            profile.instrumental_skill_level or 1,
            profile.composing_skill_level or 1,
            profile.conducting_skill_level or 1,
        ]
    elif profile.career_interests == 'sports':
        skill_assessment['labels'] = ['Playing', 'Coaching', 'Refereeing', 'Physical Training']
        skill_assessment['data'] = [
            profile.playing_skill_level or 1,
            profile.coaching_skill_level or 1,
            profile.refereeing_skill_level or 1,
            profile.physical_training_skill_level or 1,
        ]
    elif profile.career_interests == 'fashion':
        skill_assessment['labels'] = ['Fashion Designing', 'Fashion Styling', 'Fashion Illustration', 'Fashion Merchandising']
        skill_assessment['data'] = [
            profile.fashion_designing_skill_level or 1,
            profile.fashion_styling_skill_level or 1,
            profile.fashion_illustration_skill_level or 1,
            profile.fashion_merchandising_skill_level or 1,
        ]
    return skill_assessment

def get_career_recommendations(profile):
    data = {
        "bio": profile.bio,
        "skills": profile.skills,
        "career_goals": profile.career_goals,
    }

    prompt = f"Generate career recommendations for a user with the following details: {data}"

    response = model.generate_content(prompt)

    if response and hasattr(response, 'text'):
        recommendations = response.text.strip().split('\n')
        recommendations_html = generate_html_from_text(recommendations)
        return recommendations_html
    else:
        return "<p>No recommendations available.</p>"

def get_job_listings(profile):
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
def get_career_recommendations_view(request):
    profile = request.user.profile
    response = model.generate_content(f"Generate career recommendations for a user with the following details: {profile.bio}, {profile.skills}, {profile.career_goals}")

    if response and hasattr(response, 'text'):
        profile.career_recommendations = response.text
        profile.save()
        award_badge(request, 'Career Recommendation')  # Pass request object
        return JsonResponse({'status': 'success', 'career_recommendations': profile.career_recommendations})

    return JsonResponse({'status': 'error', 'message': 'Failed to generate career recommendations.'}, status=400)


@login_required
def get_job_prospects_view(request):
    profile = request.user.profile
    response = model.generate_content(f"Generate job prospects for a user with the following details: {profile.skills}, {profile.location}, {profile.career_goals}")

    if response and hasattr(response, 'text'):
        profile.job_prospects = response.text
        profile.save()
        award_badge(request, 'Job Prospect')  # Pass request object
        return JsonResponse({'status': 'success', 'job_prospects': profile.job_prospects})

    return JsonResponse({'status': 'error', 'message': 'Failed to generate job prospects.'}, status=400)


@login_required
def assess_skills(request):
    profile = request.user.profile
    response = model.generate_content(f"Assess the following skills: {profile.skills}")

    if response and hasattr(response, 'text'):
        profile.skill_assessment = response.text
        profile.save()
        award_badge(request, 'Skill Assessment')  # Pass request object
        return JsonResponse({'status': 'success', 'skill_assessment': profile.skill_assessment})

    return JsonResponse({'status': 'error', 'message': 'Failed to assess skills.'}, status=400)

@login_required
def get_resume_advice(request):
    profile = request.user.profile
    user = request.user
    resume_data = {
        "name": user.get_full_name() or user.username,
        "desired_job_title": profile.resume_job_title,
        "education": profile.resume_education,
        "skills": profile.skills,
        "professional_experience": profile.professional_experience,
        "relevant_projects": profile.resume_skills_experiences,  # Adjust field name if necessary
        "certifications_awards": profile.certifications_awards  # Ensure this field exists in your Profile model
    }

    prompt = f"""
    Give resume advice for the following profile:

    Name: {resume_data['name']}
    Desired Job Title/Field: {resume_data['desired_job_title']}
    Education Level and Relevant Coursework: {resume_data['education']}
    Skills and Abilities: {resume_data['skills']}
    Relevant Projects, Volunteer Work, or Extracurricular Activities: {resume_data['relevant_projects']}
    Certifications or Awards: {resume_data['certifications_awards']}

    Professional Experience: {resume_data['professional_experience']}
    """

    response = model.generate_content(prompt)

    if response and hasattr(response, 'text'):
        profile.resume_advice = response.text
        profile.save()
        award_badge(request, 'Resume Advice')  # Pass request object
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
        award_badge(request, 'Matched Jobs')  # Pass request object
        return JsonResponse({'status': 'success', 'matched_jobs': profile.matched_jobs})

    return JsonResponse({'status': 'error', 'message': 'Failed to match jobs.'}, status=400)

@login_required
def get_learning_resources(request):
    profile = request.user.profile
    response = model.generate_content(f"Provide learning resources for the following skills: {profile.skills}")

    if response and hasattr(response, 'text'):
        profile.learning_resources = response.text
        profile.save()
        award_badge(request, 'Learning Resources')  # Pass request object
        return JsonResponse({'status': 'success', 'learning_resources': profile.learning_resources})

    return JsonResponse({'status': 'error', 'message': 'Failed to fetch learning resources.'}, status=400)

@login_required
def find_networking_opportunities(request):
    profile = request.user.profile
    response = model.generate_content(f"Find networking opportunities for the following interests: {profile.career_goals}")

    if response and hasattr(response, 'text'):
        profile.networking_opportunities = response.text
        profile.save()
        award_badge(request, 'Networking Opportunities')  # Pass request object
        return JsonResponse({'status': 'success', 'networking_opportunities': profile.networking_opportunities})

    return JsonResponse({'status': 'error', 'message': 'Failed to fetch networking opportunities.'}, status=400)

@login_required
def dash(request):
    profile = request.user.profile

    if not profile.is_complete:
        return redirect('complete_profile_step1')

    career_progress = profile.career_progress if profile.career_progress else {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June'],
        'data': [0, 10, 5, 2, 20, 30]
    }

    skill_assessment = get_skill_assessment(profile)

    context = {
        'career_progress': json.dumps(career_progress),
        'skill_assessment': json.dumps(skill_assessment),
        'user': request.user,
        'profile': profile,
        'career_recommendations': profile.career_recommendations,
        'job_prospects': profile.job_prospects,
        'resume_advice': profile.resume_advice,
        'matched_jobs': profile.matched_jobs,
        'learning_resources': profile.learning_resources,
        'networking_opportunities': profile.networking_opportunities,
    }

    return render(request, 'dash.html', context)


def get_career_pathway(profile, max_steps=10):
    data = {
        "bio": profile.bio,
        "skills": profile.skills,
        "career_goals": profile.career_goals,
        "career_interests": profile.career_interests,
    }

    prompt = f"""
    Generate a detailed career pathway for a user with the following details:
    Bio: {data["bio"]}
    Skills: {data["skills"]}
    Career Goals: {data["career_goals"]}
    Career Interests: {data["career_interests"]}

    Provide up to {max_steps} key steps clearly and concisely as separate lines.
    """

    try:
        response = model.generate_content(prompt)
    except Exception as e:
        print(f"Error generating content: {e}")
        return {"nodes": [], "links": []}

    career_pathway = {
        'nodes': [],
        'links': []
    }

    if response and hasattr(response, 'text'):
        pathway_steps = response.text.strip().split('\n')[:max_steps]
        previous_node_id = 'start'
        career_pathway['nodes'].append({'id': previous_node_id, 'name': 'Start', 'level': 1})

        for idx, step in enumerate(pathway_steps):
            level = idx + 2
            node_id = f"step{level}"
            career_pathway['nodes'].append({'id': node_id, 'name': step.strip(), 'level': level})
            career_pathway['links'].append({'source': previous_node_id, 'target': node_id})
            previous_node_id = node_id

        profile.career_pathway = career_pathway
        profile.save()

    return career_pathway

@login_required
def career_pathway(request):
    profile = request.user.profile

    # Check if the career pathway already exists in the profile
    if not profile.career_pathway:
        career_pathway_data = get_career_pathway(profile)
    else:
        career_pathway_data = profile.career_pathway

    return render(request, 'career_pathway.html', {'career_pathway': json.dumps(career_pathway_data)})

@login_required
def generate_career_pathway(request):
    profile = request.user.profile
    career_pathway_data = get_career_pathway(profile)
    award_badge(request, 'Career Pathway')  # Pass request object
    return JsonResponse({'career_pathway': career_pathway_data})

@login_required
def learning_pathway(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'learning_path.html', {'learning_pathway': profile.learning_pathway})

@login_required
def generate_learning_pathway(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    data = {
        "bio": profile.bio,
        "skills": profile.skills,
        "career_goals": profile.career_goals,
        "career_interests": profile.career_interests,
    }

    prompt = f"""
    Based on the following details, generate a personalized learning pathway with recommended courses, certifications, and resources:
    Bio: {data["bio"]}
    Skills: {data["skills"]}
    Career Goals: {data["career_goals"]}
    Career Interests: {data["career_interests"]}
    """

    response = model.generate_content(prompt)

    learning_pathway = response.text if response and hasattr(response, 'text') else "No recommendations available."

    profile.learning_pathway = learning_pathway
    profile.save()
    award_badge(request, 'Learning Pathway')  # Pass request object
    return JsonResponse({'status': 'success', 'learning_pathway': learning_pathway})

@login_required
@require_GET
def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.none()
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(profile__skills__icontains=query) |
            Q(profile__career_interests__icontains=query) |
            Q(profile__bio__icontains=query)
        ).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        suggestions = [{'username': user.username, 'url': user.profile.get_absolute_url()} for user in users]
        return JsonResponse({'suggestions': suggestions})

    return render(request, 'search_results.html', {'users': users, 'query': query})


@login_required
def chat(request, username):
    try:
        receiver = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "The user you are trying to message does not exist.")
        return redirect('messages')
    
    chat_messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)
    ).order_by('timestamp')

    return render(request, 'chat.html', {'receiver': receiver, 'chat_messages': chat_messages})


@login_required
def user_messages(request):
    user_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('timestamp')

    conversations = {}
    for message in user_messages:
        other_user = message.receiver if message.sender == request.user else message.sender
        if other_user not in conversations or conversations[other_user].timestamp < message.timestamp:
            conversations[other_user] = message

    return render(request, 'messages.html', {'conversations': conversations})
    

from .models import Profile, Connection, ConnectionRequest, Message, Notification

@login_required
def connect(request, username):
    user_to_connect = get_object_or_404(User, username=username)
    if Connection.objects.filter(user_from=request.user, user_to=user_to_connect).exists():
        messages.info(request, 'You are already connected.')
    else:
        connection_request = Connection.objects.create(user_from=request.user, user_to=user_to_connect)
        notification = Notification.objects.create(
            user=user_to_connect,
            message=f'{request.user.username} sent you a connection request.',
            target_url=reverse('user_profile', args=[request.user.username])
        )
        messages.success(request, 'Connection request sent.')
        award_badge(request, 'Connect')  # Pass request object
    return redirect('user_profile', username=username)



@login_required
def connections_list(request, username):
    user = get_object_or_404(User, username=username)
    connections = Connection.objects.filter(user_from=user).select_related('user_to')
    return render(request, 'connections_list.html', {'connections': connections, 'profile_user': user})


@login_required
def send_connection_request(request, username):
    if request.method == 'POST':
        user_to_connect = get_object_or_404(User, username=username)
        if ConnectionRequest.objects.filter(from_user=request.user, to_user=user_to_connect).exists():
            return JsonResponse({'status': 'error', 'message': 'Connection request already sent.'})
        
        ConnectionRequest.objects.create(from_user=request.user, to_user=user_to_connect)
        send_notification(user_to_connect, f'{request.user.username} sent you a connection request.')
        award_badge(request, 'Connection Request')  # Pass request object
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)



@login_required
def accept_connection_request(request, request_id):
    connection_request = get_object_or_404(ConnectionRequest, id=request_id, to_user=request.user)
    connection_request.accept()
    Notification.objects.create(user=connection_request.from_user, message=f'{request.user.username} accepted your connection request.')
    messages.success(request, "Connection request accepted.")
    award_badge(request, 'Accept Connection')  # Pass request object
    return redirect('view_connections')

@login_required
def reject_connection_request(request, request_id):
    connection_request = get_object_or_404(ConnectionRequest, id=request_id, to_user=request.user)
    connection_request.reject()
    messages.success(request, "Connection request rejected.")
    return redirect('view_connections')

@login_required
def view_connections(request):
    user_connections = Connection.objects.filter(user_from=request.user)
    connection_requests = ConnectionRequest.objects.filter(to_user=request.user, accepted=False)
    sent_requests = ConnectionRequest.objects.filter(from_user=request.user, accepted=False)
    return render(request, 'connections.html', {
        'connections': user_connections,
        'requests': connection_requests,
        'sent_requests': sent_requests
    })

@login_required
def remove_connection(request, username):
    user_to_disconnect = get_object_or_404(User, username=username)
    
    # Remove both directions of the connection
    connection1 = Connection.objects.filter(user_from=request.user, user_to=user_to_disconnect).first()
    connection2 = Connection.objects.filter(user_from=user_to_disconnect, user_to=request.user).first()
    
    if connection1:
        connection1.delete()
    
    if connection2:
        connection2.delete()
    
    messages.success(request, 'Connection removed.')
    return redirect('connections')

@login_required
def cancel_connection_request(request, request_id):
    connection_request = get_object_or_404(ConnectionRequest, id=request_id, from_user=request.user)
    connection_request.delete()
    messages.success(request, 'Connection request cancelled.')
    return redirect('view_connections')

@login_required
def notifications(request):
    notifications = request.user.notifications.order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})

def send_notification(user, message):
    notification = Notification.objects.create(user=user, message=message)
    pusher_client.trigger(f'notifications-{user.id}', 'new-notification', {
        'message': message
    })


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('notifications')

@login_required
def fetch_notifications(request):
    notifications = request.user.notifications.filter(is_read=False).order_by('-timestamp')
    notifications_data = [
        {
            'id': notification.id,
            'message': notification.message,
            'url': notification.get_target_url()
        }
        for notification in notifications
    ]
    return JsonResponse({'notifications': notifications_data})


@login_required
def settings(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = PrivacySettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully.')
            return redirect('settings')
    else:
        form = PrivacySettingsForm(instance=profile)
    return render(request, 'settings.html', {'form': form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm'] == 'DELETE':
            user = request.user
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('home')
    else:
        form = DeleteAccountForm()
    return render(request, 'delete_account.html', {'form': form})

@login_required
def privacy(request):
    return render(request, 'privacy.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')

@login_required
@require_POST
def submit_feedback(request):
    if request.method == 'POST':
        recommendation = request.POST.get('recommendation')
        job_listing = request.POST.get('job_listing')
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')

        Feedback.objects.create(
            user=request.user,
            recommendation=recommendation,
            job_listing=job_listing,
            feedback_text=feedback_text,
            rating=rating
        )
        award_badge(request, 'Feedback Submitted')  # Pass request object
        return JsonResponse({'status': 'success', 'message': 'Thank you for your feedback!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@login_required
@require_GET
def user_feedback(request):
    feedback_list = Feedback.objects.filter(user=request.user)
    return render(request, 'user_feedback.html', {'feedback_list': feedback_list})

@login_required
def resume_advice(request):
    return render(request, 'resume_advice.html')  # Ensure you have this template

@login_required
def get_resume_advice_from_file(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        resume_file = request.FILES['resume']
        
        # Save the resume file temporarily
        file_path = default_storage.save('tmp/' + resume_file.name, ContentFile(resume_file.read()))
        file_full_path = os.path.join(project_settings.MEDIA_ROOT, file_path)
        
        try:
            # Extract text from resume using a library like PyMuPDF for PDF or python-docx for DOCX
            if resume_file.name.endswith('.pdf'):
                import fitz  # PyMuPDF
                doc = fitz.open(file_full_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()  # Make sure to close the file
            elif resume_file.name.endswith('.docx'):
                import docx
                doc = docx.Document(file_full_path)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            else:
                return JsonResponse({'status': 'error', 'message': 'Unsupported file type.'}, status=400)
            
            # Delete the temporary file
            default_storage.delete(file_path)

            # Generate resume advice using AI
            prompt = f"Give resume advice for the following resume content:\n\n{text}"
            response = model.generate_content(prompt)

            if response and hasattr(response, 'text'):
                resume_advice = response.text
                award_badge(request, 'Resume Advice from File')  # Pass request object
                return JsonResponse({'status': 'success', 'resume_advice': resume_advice})

            return JsonResponse({'status': 'error', 'message': 'Failed to generate resume advice.'}, status=400)
        except Exception as e:
            default_storage.delete(file_path)  # Ensure file is deleted even if there's an error
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

@login_required
def badges(request):
    badges = UserBadge.objects.filter(user=request.user).select_related('badge')
    return render(request, 'badges.html', {'badges': badges})

def award_badge(request, badge_name):
    try:
        badge = Badge.objects.get(name=badge_name)
        UserBadge.objects.get_or_create(user=request.user, badge=badge)
        pusher_client.trigger(f'notifications-{request.user.id}', 'new-notification', {'message': f'You have been awarded the {badge.name} badge!'})
    except ObjectDoesNotExist:
        logger.error(f"Badge with name '{badge_name}' does not exist.")
        messages.error(request, f"Badge with name '{badge_name}' does not exist.")

@login_required
def find_people(request):
    profile = request.user.profile
    career_interest = profile.career_interests

    # Find people with the same career interest
    people = Profile.objects.filter(career_interests=career_interest).exclude(user=request.user)

    context = {
        'people': people,
        'career_interest': career_interest,
    }

    return render(request, 'find_people.html', context)
