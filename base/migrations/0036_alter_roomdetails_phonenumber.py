# Generated by Django 5.0.7 on 2024-12-01 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0035_alter_roomdetails_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomdetails',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]