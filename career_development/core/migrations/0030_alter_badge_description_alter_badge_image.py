# Generated by Django 5.0.6 on 2024-08-07 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_rename_awarded_at_userbadge_awarded_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='description',
            field=models.TextField(default='Default description for badge'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='badge',
            name='image',
            field=models.ImageField(default='Default', upload_to='badges/'),
            preserve_default=False,
        ),
    ]