# Generated by Django 5.0.6 on 2024-07-09 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_profile_certifications_awards'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='career_interests',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='career_progress',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='career_recommendations',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='job_prospects',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='learning_resources',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='matched_jobs',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='networking_opportunities',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='resume_advice',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='skill_assessment',
        ),
        migrations.AddField(
            model_name='profile',
            name='finance_skill_level',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='management_skill_level',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='marketing_skill_level',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='sales_skill_level',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='css_skill_level',
            field=models.CharField(blank=True, default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='django_skill_level',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='html_skill_level',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='js_skill_level',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='python_skill_level',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='resume_job_title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
