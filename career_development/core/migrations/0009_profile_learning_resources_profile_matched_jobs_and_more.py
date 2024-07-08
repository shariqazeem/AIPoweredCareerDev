# Generated by Django 5.0.6 on 2024-07-08 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_profile_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='learning_resources',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='matched_jobs',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='networking_opportunities',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='resume_advice',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='skill_assessment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
