# Generated by Django 5.0.7 on 2024-11-01 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_registrationdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]