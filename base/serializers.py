from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Assuming you have a Profile model for additional user information
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['id','user','name','phone_number', 'role']


class ProfileSerializer(serializers.ModelSerializer):
    userType = serializers.CharField(source='userType.name', read_only=True)  # Serialize the name of the userType

    class Meta:
        model = Profile
        fields = ['id', 'user', 'phone_number', 'userType']

        
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    profile = ProfileSerializer(read_only=True)  # Nested serializer for Profile

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'token', 'profile']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class MessageSerializer(serializers.ModelSerializer):

    receiver_profile = ProfileSerializer(read_only=True)
    sender_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id','user','sender','sender_profile','receiver','receiver_profile','message','is_read','date']