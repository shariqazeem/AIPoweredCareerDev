from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile and not profile.is_complete:
                allowed_paths = [
                    reverse('complete_profile_step1'),
                    reverse('complete_profile_step2'),
                    reverse('complete_profile_step3'),
                    reverse('logout')  # Allow logout path
                ]
                if request.path not in allowed_paths:
                    return redirect('complete_profile_step1')

        response = self.get_response(request)
        return response
