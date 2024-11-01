from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view ,permission_classes,parser_classes
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.db.models import Subquery, OuterRef , Q
from rest_framework import generics,status
from .models import *


from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from . models import *
# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return (Response(serializer.data))

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getUserType(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile,many=False)
    return Response(serializer.data['userType'])

@api_view(['GET'])
def getRegistrationDetails(request):
    user = request.user
    details = RegistrationDetails.objects.get(user=user)
    serializer = RegisterDetailsSerializer(details,many=False)
    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):
    data = request.data

    # Create the user
    user = User.objects.create_user(
        first_name=data['name'],
        email=data['email'],
        username=data['username'],
        password=data['password'],
    )

    dataInstance = UserType.objects.get(name=data['userType'])
    # Create a profile for additional fields
    profile = Profile.objects.create(
        user=user,
        phone_number=data['phone_number'],
        userType=dataInstance,
    )

    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)


class MyInbox(generics.ListAPIView):

    
    serializer_class = MessageSerializer 

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        messages = ChatMessage.objects.filter(
            id__in = Subquery(
                User.objects.filter(
                    Q(sender__receiver= user_id|Q(receiver__sender=user_id))
                ).distinct()
                .annotate(
                    last_message= Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'),receiver=user_id)|
                            Q(sender=user_id,receiver=OuterRef('id'))
                        ).order_by("-id")[:1].values_list("id",flat=True)
                    )
                ).values_list("last_message",flat=True).order_by("-id")
            )
        ).order_by("-id")

        return messages



class GetMessages(generics.ListAPIView):
    serializer_class = ChatMessage

    def get_queryset(self):
        sender_id = self.kwargs[sender_id]
        receciver_id = self.kwargs[receciver_id]

        messages = ChatMessage.objects.filter(
            sender__in=[sender_id,receciver_id],
            receciver_id=[receciver_id,sender_id]
        )

        return messages
    
class SendMessage(generics.CreateAPIView):
    serializer_class = MessageSerializer

class ProfileDetail(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all
    permission_classes = [IsAuthenticated]

class SearchUser(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        # logged_in_user = self.request.user
        users = Profile.objects.filter(
            Q(user__username__icontains= username)|
            Q(user__name__icontains= username)|
            Q(user__email__icontains= username)
        ) 

        if not users.exists():
            return Response({"details":"No users found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(users,many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])  # Allow parsing of file data
def verify_user(request):
    user = request.user  # Get the currently logged-in user
    print(user)


    # Check if user already has registration details
    if RegistrationDetails.objects.filter(user=user).exists():
        print('haha')
        return Response({"detail": "User already has registration details."}, status=status.HTTP_400_BAD_REQUEST)

    data = {
        'name': request.data.get('name'),
        'image': request.data.get('image'),
        'image1': request.data.get('image1'),
        'image2': request.data.get('image2'),
        'image3': request.data.get('image3'),
        'user': user.id  # Add the user ID
    }
    print("Incoming request data:", data)
    # Initialize the serializer with data and context
    serializer = RegisterVerifySerializer(data=data)

    # Validate and save if data is valid
    if serializer.is_valid():
        serializer.save(user=user)  # Automatically associate the `user` field
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Log the serializer errors for debugging
    print(serializer.errors)  # Add this line for debugging
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

