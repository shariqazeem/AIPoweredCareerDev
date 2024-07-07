# Generated by Django 5.0.6 on 2024-06-22 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_profile_career_goals_profile_professional_experience_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='career_goals',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='profile',
            name='professional_experience',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
