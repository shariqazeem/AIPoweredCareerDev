from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.http import JsonResponse
from .forms import UserUpdateForm, ProfileUpdateForm
from .forms import UserUpdateForm, ProfileUpdateForm, ProfileStep1Form, ProfileStep2Form, ProfileStep3Form
from .models import Resource, Connection, User, Profile
from django.contrib.auth.forms import UserCreationForm
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

# Initialize the GenAI client using the configured API key
import google.generativeai as genai

# Initialize the GenAI client using the configured API key
genai.configure(api_key=settings.GEMINI_API_KEY)

# Create the model with specific generation configuration
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
    # Your logic for rendering the home page
    return render(request, 'home.html')

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input w-full'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input w-full'})
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields
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

from django.contrib.auth import authenticate
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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


from django.utils.encoding import force_str

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
    # Redirect to a success page (login page, for example)
    return redirect('login')

@login_required
def dashboard(request):
    recommendations = get_career_recommendations(request.user)
    job_listings = get_job_listings(request.user)
    return render(request, 'dashboard.html', {
        'user': request.user,
        'recommendations': recommendations,
        'job_listings': job_listings
    })

@login_required
def complete_profile_step1(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileStep1Form(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('complete_profile_step2')
    else:
        form = ProfileStep1Form(instance=profile)
    return render(request, 'account/complete_profile_step1.html', {'form': form})

@login_required
def complete_profile_step2(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileStep2Form(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('complete_profile_step3')
    else:
        form = ProfileStep2Form(instance=profile)
    return render(request, 'account/complete_profile_step2.html', {'form': form})

@login_required
def complete_profile_step3(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileStep3Form(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile setup completed successfully.')
            return redirect('profile')
    else:
        form = ProfileStep3Form(instance=profile)
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

        # Check if profile is complete
        if profile_form.is_valid():
            return redirect('profile_details')  # Redirect to complete profile details

    recommendations = get_career_recommendations(request.user)
    job_listings = get_job_listings(request.user)

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

# Other views remain unchanged...

# Other views remain unchanged...


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
        return response.text.strip().split('\n')
    else:
        return []

from .models import Profile

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
        return response.text.strip().split('\n')
    else:
        return []

@login_required
def career_recommendations(request):
    recommendations = get_career_recommendations(request.user)
    return render(request, 'career_recommendations.html', {'recommendations': recommendations})

@login_required
def job_prospects(request):
    job_listings = get_job_listings(request.user)
    return render(request, 'job_prospects.html', {'job_listings': job_listings})


def assess_skills(request):
    if request.method == 'POST':
        user_skills = request.POST.get('skills', '')
        response = model.generate_embeddings(content=user_skills)

        if response and response.status_code == 200:
            data = response.json()
            return JsonResponse({'status': 'success', 'message': 'Skills assessed successfully.', 'data': data})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to assess skills.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def get_resume_advice(request):
    if request.method == 'GET':
        user_resume_text = request.GET.get('resume_text', '')
        response = model.generate_content(
            prompt=f"Give resume advice for the following text: {user_resume_text}"
        )

        if response and hasattr(response, 'text'):
            return JsonResponse({'status': 'success', 'message': 'Resume advice generated successfully.', 'data': response.text})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to generate resume advice.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def match_jobs(request):
    if request.method == 'POST':
        user_data = {
            'skills': request.POST.get('skills', ''),
            'location': request.POST.get('location', ''),
            'career_goals': request.POST.get('career_goals', '')
        }
        response = model.generate_content(
            prompt=f"Match jobs for a user with the following details: {user_data}"
        )

        if response and hasattr(response, 'text'):
            return JsonResponse({'status': 'success', 'message': 'Job matching successful.', 'data': response.text})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to match jobs.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def get_learning_resources(request):
    if request.method == 'GET':
        user_skills = request.GET.get('skills', '')
        response = model.generate_content(
            prompt=f"Provide learning resources for the following skills: {user_skills}"
        )

        if response and hasattr(response, 'text'):
            return JsonResponse({'status': 'success', 'message': 'Learning resources fetched successfully.', 'data': response.text})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to fetch learning resources.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def find_networking_opportunities(request):
    if request.method == 'GET':
        user_interests = request.GET.get('interests', '')
        response = model.generate_content(
            prompt=f"Find networking opportunities for the following interests: {user_interests}"
        )

        if response and hasattr(response, 'text'):
            return JsonResponse({'status': 'success', 'message': 'Networking opportunities fetched successfully.', 'data': response.text})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to fetch networking opportunities.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
