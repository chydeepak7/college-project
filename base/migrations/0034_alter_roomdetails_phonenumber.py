# Generated by Django 5.0.7 on 2024-12-01 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_alter_roomdetails_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomdetails',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
