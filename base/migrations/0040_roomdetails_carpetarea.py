# Generated by Django 5.0.7 on 2024-12-01 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0039_roomdetails_floorno_roomdetails_houseage'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomdetails',
            name='carpetArea',
            field=models.IntegerField(default=0),
        ),
    ]
