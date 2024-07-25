from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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
    skill_assessment = models.JSONField(blank=True, default=dict, null=True)
    skill_levels = models.JSONField(blank=True, default=dict, null=True)
    resume_advice = models.TextField(blank=True, default='')
    matched_jobs = models.JSONField(blank=True, default=dict, null=True)
    learning_resources = models.JSONField(blank=True, default=dict, null=True)
    networking_opportunities = models.JSONField(blank=True, default=dict, null=True)
    career_recommendations = models.JSONField(blank=True, default=dict, null=True)
    job_prospects = models.JSONField(blank=True, default=dict, null=True)
    career_progress = models.JSONField(blank=True, default=dict, null=True)
    certifications_awards = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    career_pathway = models.JSONField(blank=True, default=dict, null=True)
    learning_pathway = models.TextField(blank=True, default='')
    private = models.BooleanField(default=False)  # New field to make profile private

    # Technology Skills
    html_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    css_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    js_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    python_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    django_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    nodejs_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    php_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    java_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    csharp_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    cpp_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    sql_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    react_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    angular_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])

    # Business Skills
    management_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    marketing_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    finance_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    sales_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    accounting_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    hr_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    operations_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    strategic_planning_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])

    # Arts Skills
    drawing_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    painting_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    sculpting_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    photography_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    graphic_design_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    illustration_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    animation_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    printmaking_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])

    # Music Skills
    singing_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    instrumental_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    composing_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    conducting_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    music_production_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    music_theory_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    djing_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    sound_engineering_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])

    # Sports Skills
    playing_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    coaching_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    refereeing_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    physical_training_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    nutrition_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    physiotherapy_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    sports_management_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])

    # Fashion Skills
    fashion_designing_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    fashion_styling_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    fashion_illustration_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    fashion_merchandising_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    textile_design_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    pattern_making_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    sewing_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    fashion_marketing_skill_level = models.IntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'username': self.user.username})

    @property
    def is_complete(self):
        # Bypass the check for superusers
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
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_from', 'user_to')

class ConnectionRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def accept(self):
        self.accepted = True
        self.save()
        Connection.objects.get_or_create(user_from=self.from_user, user_to=self.to_user)
        Connection.objects.get_or_create(user_from=self.to_user, user_to=self.from_user)

    def reject(self):
        self.delete()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Add this line

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    target_url = models.URLField(blank=True, null=True)  # allow blank or null if URL is not always needed

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"

    def get_target_url(self):
        return self.target_url if self.target_url else reverse('notifications')
