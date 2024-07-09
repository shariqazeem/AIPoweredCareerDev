# models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    career_interests = models.CharField(max_length=255, blank=True)
    skills = models.CharField(max_length=255, blank=True)
    career_goals = models.TextField(blank=True)
    professional_experience = models.TextField(blank=True)
    resume_job_title = models.CharField(max_length=100, blank=True, null=True)
    resume_skills_experiences = models.TextField(blank=True)
    resume_education = models.TextField(blank=True)
    skill_assessment = models.JSONField(blank=True, default=dict)
    skill_levels = models.JSONField(blank=True, default=dict)
    resume_advice = models.TextField(blank=True, default='')
    matched_jobs = models.JSONField(blank=True, default=dict)
    learning_resources = models.JSONField(blank=True, default=dict)
    networking_opportunities = models.JSONField(blank=True, default=dict)
    career_recommendations = models.JSONField(blank=True, default=dict)
    job_prospects = models.JSONField(blank=True, default=dict)
    career_progress = models.JSONField(blank=True, default=dict)
    certifications_awards = models.TextField(blank=True)

    html_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    css_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    js_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    python_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    django_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])

    def __str__(self):
        return self.user.username

    @property
    def is_complete(self):
        if self.user.is_superuser:
            return True
        required_fields = ['bio', 'location', 'career_interests', 'skills', 'career_goals', 'professional_experience']
        for field in required_fields:
            if not getattr(self, field):
                return False
        return True


class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.title

class Connection(models.Model):
    user_from = models.ForeignKey(User, related_name='connections_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='connections_to', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_from} -> {self.user_to}"
