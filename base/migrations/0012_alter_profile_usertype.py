# Generated by Django 5.0.6 on 2024-08-28 10:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_remove_profile_role_profile_usertype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='userType',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='base.usertype'),
        ),
    ]