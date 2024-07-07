from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('complete-profile/step1/', views.complete_profile_step1, name='complete_profile_step1'),
    path('complete-profile/step2/', views.complete_profile_step2, name='complete_profile_step2'),
    path('complete-profile/step3/', views.complete_profile_step3, name='complete_profile_step3'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('career-recommendations/', views.career_recommendations, name='career_recommendations'),
    path('job-prospects/', views.job_prospects, name='job_prospects'),
    path('resources/', views.resources, name='resources'),
    path('connect/<username>/', views.connect, name='connect'),
    path('connections/', views.connections, name='connections'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user/<username>/', views.user_profile, name='user_profile'),
]
