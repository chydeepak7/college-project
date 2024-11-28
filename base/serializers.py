from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Assuming you have a Profile model for additional user information
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    userType = serializers.CharField(source='userType.name', read_only=True)  # Serialize the name of the userType

    class Meta:
        model = Profile
        fields = ['user', 'phone_number', 'userType', 'is_verified']


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ['name']


# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['id','user','name','phone_number', 'role']




# class ProfileListSerializer(serializers.ModelSerializer):
#     profile = ProfileSerializer()
#     class Meta:
#         model =





# class MessageSerializer(serializers.ModelSerializer):
#
#     receiver_profile = ProfileSerializer(read_only=True)
#     sender_profile = ProfileSerializer(read_only=True)
#
#     class Meta:
#         model = ChatMessage
#         fields = ['id','user','sender','sender_profile','receiver','receiver_profile','message','is_read','date']
#         # extra_kwargs = {
#         #     'user': {'read_only': True},  # Set user to read-only if it's derived from sender
#         #     'sender': {'write_only': True},
#         #     'receiver': {'write_only': True},
#         #     'message': {'write_only': True},
#         #     'is_read': {'default': False},  # Defaults to False if not provided
#         # }



class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    receiver_name = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = ChatMessage
        fields = '__all__'








class RegisterDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationDetails
        fields = '__all__'


class RegisterVerifySerializer(serializers.ModelSerializer):
    # Explicitly declare image fields to handle file uploads
    passportPhoto = serializers.ImageField(required=False,allow_null=True)
    citizenshipFront = serializers.ImageField(required=False,allow_null=True)
    citizenshipBack = serializers.ImageField(required=False,allow_null=True)
    # image3 = serializers.ImageField(required=False,allow_null=True)

    class Meta:
        model = RegistrationDetails
        fields = '__all__'
        # read_only_fields = ['user']  #
        def create(self, validated_data):
            user = validated_data.pop('user')  # Extract the user from validated data
            registration_detail = RegistrationDetails.objects.create(user=user, **validated_data)
            return registration_detail



class RoomDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomDetails
        fields = '__all__'




class AddRoom(serializers.ModelSerializer):
    # Explicitly declare image fields to handle file uploads
    image = serializers.ImageField(required=False,allow_null=True)
    image1 = serializers.ImageField(required=False,allow_null=True)
    image2 = serializers.ImageField(required=False,allow_null=True)
    image3 = serializers.ImageField(required=False,allow_null=True)

    class Meta:
        model = RoomDetails
        fields = '__all__'
        # read_only_fields = ['user']  #
        def create(self, validated_data):
            user = validated_data.pop('user')  # Extract the user from validated data
            room_detail = RoomDetails.objects.create(user=user, **validated_data)
            return room_detail


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    registerVerify = RegisterDetailsSerializer(source='registrationdetails', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'registerVerify']




class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    profile = ProfileSerializer(read_only=True)  # Nested serializer for Profile

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'token', 'profile']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)