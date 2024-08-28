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
#         return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    phone_number = models.CharField(max_length=15,default=None)
    userType = models.ForeignKey(UserType, on_delete=models.CASCADE, default=None) # 'Landlord' or 'Tenant' 

    def __str__(self):
        return self.user.username
    
class ChatMessage(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")

    message = models.CharField(max_length= 1000)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name_plural = "Message"
    
    def __str__(self):
        return f"{self.sender} - {self.receiver}"

    @property
    def sender_profile(self):
        sender_profile = Profile.objects.get(user=self.sender)
        return sender_profile
    
    @property
    def receiver_profile(self):
        receiver_profile = Profile.objects.get(user=self.receiver)
        return receiver_profile
    


