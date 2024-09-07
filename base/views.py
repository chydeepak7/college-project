from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.db.models import Subquery, OuterRef , Q
from rest_framework import generics,status


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
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


# @api_view(['POST'])
# def registerUser(request):
#     data = request.data

#     # Check if passwords match
#     if data['password'] != data['confirm_password']:
#         return Response({'detail': 'Passwords do not match'}, status=400)

#     user = User.objects.create(
#         full_name=data['first_name'],
#         email=data['email'],
#         username=data['username'],
#         password=data['password'],
#     )

#     # Create a profile for additional fields
#     Profile.objects.create(
#         user=user,
#         phone_number=data['phone_number'],
#         role=data['role'],  # Landlord or Tenant
#     )

#     serializer = UserSerializerWithToken(user, many=False)
#     return Response(serializer.data)


@api_view(['POST'])
def registerUser(request):
    data = request.data

    # Check if passwords match
    if data['password'] != data['confirm_password']:
        return Response({'detail': 'Passwords do not match'}, status=400)

    try:
        userType = UserType.objects.get(name=data['role'])
    except UserType.DoesNotExist:
        return Response({'detail': 'Invalid role'}, status=400)

    # Create the user
    user = User.objects.create_user(
        first_name=data['full_name'],
        email=data['email'],
        username=data['username'],
        password=data['password'],
    )

    # Create a profile for additional fields
    Profile.objects.create(
        user=user,
        phone_number=data['phone_number'],
        userType=userType,
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