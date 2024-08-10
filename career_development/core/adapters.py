# core/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # This is called after a successful login attempt
        # Check if the social account's email address already exists
        email_address = sociallogin.account.extra_data['email']
        try:
            existing_user = User.objects.get(email=email_address)
            if existing_user:
                # If the user already exists, link the social account to the existing user
                sociallogin.connect(request, existing_user)
                messages.info(request, "This email is already associated with an account. We've linked the Google account to your existing account.")
        except User.DoesNotExist:
            pass
