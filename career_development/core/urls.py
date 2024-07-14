from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assess-skills/', views.assess_skills, name='assess_skills'),
    path('get-resume-advice/', views.get_resume_advice, name='get_resume_advice'),
    path('match-jobs/', views.match_jobs, name='match_jobs'),
    path('get-learning-resources/', views.get_learning_resources, name='get_learning_resources'),
    path('find-networking-opportunities/', views.find_networking_opportunities, name='find_networking_opportunities'),
    path('get-career-recommendations/', views.get_career_recommendations, name='get_career_recommendations'),
    path('get-job-prospects/', views.get_job_prospects, name='get_job_prospects'),
    path('complete-profile-step1/', views.complete_profile_step1, name='complete_profile_step1'),
    path('complete-profile-step2/', views.complete_profile_step2, name='complete_profile_step2'),
    path('complete-profile-step3/', views.complete_profile_step3, name='complete_profile_step3'),
    path('complete-profile-step4/', views.complete_profile_step4, name='complete_profile_step4'),
    path('profile/', views.profile, name='profile'),
    path('profile-details/', views.profile_details, name='profile_details'),
    path('user-profile/<str:username>/', views.user_profile, name='user_profile'),
    path('resources/', views.resources, name='resources'),
    path('connect/<str:username>/', views.connect, name='connect'),
    path('connections/', views.connections, name='connections'),
    path('career-recommendations/', views.career_recommendations, name='career_recommendations'),
    path('job-prospects/', views.job_prospects, name='job_prospects'),
    path('dash/', views.dash, name='dash'),
    path('career_pathway/', views.career_pathway, name='career_pathway'),
    path('generate_career_pathway/', views.generate_career_pathway, name='generate_career_pathway'),
    path('learning_pathway/', views.learning_pathway, name='learning_pathway'),
    path('generate_learning_pathway/', views.generate_learning_pathway, name='generate_learning_pathway'),
    path('search/', views.search_users, name='search_users'),
    path('chat/<str:username>/', views.chat, name='chat'),
    path('messages/', views.messages, name='messages'),
    path('ajax_search/', views.search_users, name='ajax_search_users'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
