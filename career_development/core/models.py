from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True)
    career_goals = models.TextField(blank=True)
    professional_experience = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    # Add any additional fields here if needed

    @property
    def is_complete(self):
        required_fields = ['bio', 'skills', 'career_goals', 'professional_experience', 'location']
        for field in required_fields:
            if not getattr(self, field):
                return False
        return True
    
    def __str__(self):
        return self.user.username




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
