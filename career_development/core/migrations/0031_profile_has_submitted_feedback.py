# Generated by Django 5.0.6 on 2024-08-09 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_alter_badge_description_alter_badge_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='has_submitted_feedback',
            field=models.BooleanField(default=False),
        ),
    ]
