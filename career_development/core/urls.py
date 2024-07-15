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
    path('get_career_recommendations/', views.get_career_recommendations_view, name='get_career_recommendations_view'),
    path('get_job_prospects/', views.get_job_prospects_view, name='get_job_prospects_view'),
    path('complete-profile-step1/', views.complete_profile_step1, name='complete_profile_step1'),
    path('complete-profile-step2/', views.complete_profile_step2, name='complete_profile_step2'),
    path('complete-profile-step3/', views.complete_profile_step3, name='complete_profile_step3'),
    path('complete-profile-step4/', views.complete_profile_step4, name='complete_profile_step4'),
    path('profile/', views.profile, name='profile'),
    path('profile-details/', views.profile_details, name='profile_details'),
    path('user-profile/<str:username>/', views.user_profile, name='user_profile'),
    path('resources/', views.resources, name='resources'),
    path('connect/<str:username>/', views.send_connection_request, name='send_connection_request'),
    path('accept_request/<int:request_id>/', views.accept_connection_request, name='accept_connection_request'),
    path('reject_request/<int:request_id>/', views.reject_connection_request, name='reject_connection_request'),
    path('connections/', views.view_connections, name='view_connections'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark_read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),   
    path('career-recommendations/', views.career_recommendations, name='career_recommendations'),
    path('job-prospects/', views.job_prospects, name='job_prospects'),
    path('dash/', views.dash, name='dash'),
    path('career_pathway/', views.career_pathway, name='career_pathway'),
    path('generate_career_pathway/', views.generate_career_pathway, name='generate_career_pathway'),
    path('learning_pathway/', views.learning_pathway, name='learning_pathway'),
    path('generate_learning_pathway/', views.generate_learning_pathway, name='generate_learning_pathway'),
    path('search/', views.search_users, name='search_users'),
    path('chat/<str:username>/', views.chat, name='chat'),
    path('messages/', views.user_messages, name='user_messages'),
    path('ajax_search/', views.search_users, name='ajax_search_users'),
    path('connections/<str:username>/', views.connections_list, name='connections_list'),
    path('fetch-notifications/', views.fetch_notifications, name='fetch_notifications'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
