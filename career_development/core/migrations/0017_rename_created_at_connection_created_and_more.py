# Generated by Django 5.0.6 on 2024-07-14 22:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_message'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='connection',
            old_name='created_at',
            new_name='created',
        ),
        migrations.AlterUniqueTogether(
            name='connection',
            unique_together={('user_from', 'user_to')},
        ),
    ]
