# career_development/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Include core app URLs
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('allauth.urls')),  # Include Allauth URLs
]
