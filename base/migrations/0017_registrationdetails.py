# Generated by Django 5.0.7 on 2024-10-28 20:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_delete_registrationdetails'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
