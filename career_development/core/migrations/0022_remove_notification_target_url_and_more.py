# Generated by Django 5.0.6 on 2024-07-15 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_notification_target_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='target_url',
        ),
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('connection', 'Connection'), ('general', 'General')], default='general', max_length=50),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(),
        ),
    ]
