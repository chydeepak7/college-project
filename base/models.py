from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=100)
    numOfRoom = models.IntegerField()
    address = models.CharField(max_length=100)
    water = models.BooleanField()
    electricity = models.BooleanField()
    wifi = models.CharField(max_length=100)
    bathroom = models.CharField(max_length=100)
    otherDetails = models.CharField(max_length=100)

    def __str__(self):
        return self.address





