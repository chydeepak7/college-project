from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    numOfRoom = models.IntegerField()
    address = models.CharField(max_length=100)
    water = models.BooleanField()
    electricity = models.BooleanField()
    wifi = models.CharField(max_length=100)
    bathroom = models.CharField(max_length=100)
    otherDetails = models.CharField(max_length=100)
    createdAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.address





