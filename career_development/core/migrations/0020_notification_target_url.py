# Generated by Django 5.0.6 on 2024-07-14 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='target_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
