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
    wifi = models.BooleanField()
    bathroom = models.CharField(max_length=100)
    otherDetails = models.CharField(max_length=500)
    listedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.address

class UserType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE,default=None)
#     userType = models.OneToOneField(UserType, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.user


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    phone_number = models.CharField(max_length=15,default=None)
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE, default=None) # 'Landlord' or 'Tenant'
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# models.py
from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.sender} - {self.receiver}"


class RegistrationDetails(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    marital_status = models.CharField(max_length=50, null=True, blank=True)
    spouse_name = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    permanent_address = models.TextField(null=True, blank=True)
    passportPhoto = models.ImageField(upload_to="images/",blank=True,null=True)
    citizenshipFront = models.ImageField(upload_to="images/",blank=True,null=True)
    citizenshipBack = models.ImageField(upload_to="images/",blank=True,null=True)


    def __str__(self):
        return self.name


class RoomDetails(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    number_of_rooms = models.IntegerField()
    rent = models.IntegerField(default=0)
    bathroom = models.CharField(max_length=100,blank=True,null=True)
    phoneNumber = models.IntegerField(null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/rooms/", blank=True, null=True)
    image1 = models.ImageField(upload_to="images/rooms/", blank=True, null=True)
    image2 = models.ImageField(upload_to="images/rooms/", blank=True, null=True)
    image3 = models.ImageField(upload_to="images/rooms/", blank=True, null=True)
    other_details = models.CharField(max_length=500,blank=True,null=True)
    def __str__(self):
        return self.address


