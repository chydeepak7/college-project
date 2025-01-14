import base64

from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view ,permission_classes,parser_classes
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.db.models import Subquery, OuterRef , Q
from rest_framework import generics,status
from .models import *
from hashlib import sha256
import hashlib
from decimal import Decimal

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
def userList(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)
    return Response(serializer.data)


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
    print(user,data['phone_number'], dataInstance)
    profile = Profile.objects.create(
        user=user,
        phone_number=data['phone_number'],
        userType=dataInstance,
    )

    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)


# class MyInbox(generics.ListAPIView):
#     serializer_class = MessageSerializer
#
#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         messages = ChatMessage.objects.filter(
#             id__in=Subquery(
#                 User.objects.filter(
#                     Q(sender__receiver=user_id) | Q(receiver__sender=user_id)
#                 )
#                 .distinct()
#                 .annotate(
#                     last_message=Subquery(
#                         ChatMessage.objects.filter(
#                             Q(sender=OuterRef('id'), receiver=user_id) |
#                             Q(sender=user_id, receiver=OuterRef('id'))
#                         ).order_by("-id")[:1].values_list("id", flat=True)
#                     )
#                 )
#                 .values_list("last_message", flat=True)
#                 .order_by("-id")
#             )
#         ).order_by("-id")
#         return messages



# class GetMessages(generics.ListAPIView):
#     serializer_class = MessageSerializer
#
#     def get_queryset(self):
#         sender_id = self.kwargs['sender_id']
#         receiver_id = self.kwargs['receiver_id']
#
#         messages = ChatMessage.objects.filter(
#            Q(sender_id=sender_id, receiver_id=receiver_id) or
#             Q(sender_id=receiver_id, receiver_id=sender_id)
#         ).order_by("id")
#         return messages
#
# class SendMessage(generics.CreateAPIView):
#     serializer_class = MessageSerializer

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
        'name': request.data.get('fullName'),
        'date_of_birth': request.data.get('dateOfBirth'),
        'gender': request.data.get('gender'),
        'father_name': request.data.get('fatherName'),
        'marital_status': request.data.get('maritalStatus'),
        'spouse_name': request.data.get('spouseName'),
        'occupation': request.data.get('occupation'),
        'phone_number': request.data.get('phoneNumber'),
        'email': request.data.get('email'),
        'permanent_address': request.data.get('permanentAddress'),
        'passportPhoto': request.data.get('passportPhoto'),
        'citizenshipFront': request.data.get('citizenshipFront'),
        'citizenshipBack': request.data.get('citizenshipBack'),
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


@api_view(['GET'])
def room_details(request):
    rooms = RoomDetails.objects.all()
    serializer = RoomDetailsSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def room_detail(request):
    user = request.user
    rooms = RoomDetails.objects.filter(user=user)
    serializer = RoomDetailsSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def add_rooms(request):
    user = request.user
    data = {
        'number_of_rooms': float(request.data.get('number_of_rooms')),
        'rent': float(request.data.get('rent')),
        'carpetArea': float(request.data.get('carpetArea')),
        'phoneNumber': int(request.data.get('phoneNumber')),
        'bhk': int(request.data.get('bhk')),
        'floorNo': int(request.data.get('floorNo')),
        'houseAge': int(request.data.get('houseAge')),
        'bathroom': request.data.get('bathroom'),
        'roomFlat': request.data.get('roomFlat'),
        'other_details': request.data.get('otherDetails'),
        'address': request.data.get('address'),
        'latitude': float(request.data.get('longitude')),
        'longitude': float(request.data.get('latitude')),
        'image': request.data.get('image'),
        'image1': request.data.get('image1'),
        'image2': request.data.get('image2'),
        'image3': request.data.get('image3'),
        'user': user.id  # Add the user ID
    }
    print(data)
    serializer = RoomDetailsSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user)  # Automatically associate the `user` field
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Log the serializer errors for debugging
    print(serializer.errors)  # Add this line for debugging
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def toggle_verify_user(request, user_id):
    try:
        # Retrieve the Profile instance related to the User
        profile = Profile.objects.get(user__id=user_id)
        # Toggle the `is_verified` status
        profile.is_verified = not profile.is_verified
        profile.save()
        # Return the updated profile details
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)



# ////////////////////////////////////////
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer


    def perform_create(self, serializer):
        sender = self.request.user
        receiver_id = self.request.data.get('receiver')
        serializer.save(sender=sender, receiver_id=receiver_id)





@api_view(['GET'])
def get_chat_users(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'detail': 'Not authenticated'}, status=401)

    # Get unique users from sent and received messages
    sent_users = ChatMessage.objects.filter(sender=user).values_list('receiver', flat=True)
    received_users = ChatMessage.objects.filter(receiver=user).values_list('sender', flat=True)
    unique_user_ids = set(sent_users).union(set(received_users))

    # Get user details
    users = User.objects.filter(id__in=unique_user_ids)
    user_data = [{'id': user.id, 'name': user.username} for user in users]

    return Response(user_data)


@api_view(['POST'])
def handle_rent(request):
    try:
        # Print request data for debugging
        print("Request Data:", request.data)

        rent_id = request.data.get("rent_id")
        rent_from = request.data.get("rent_from")
        rent_to = request.data.get("rent_to")
        rent = request.data.get("rent", False)

        if not rent_id or not rent_from or not rent_to:
            return Response(
                {"success": False, "message": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        room = RoomDetails.objects.get(id=rent_id)
        # room = RoomDetails.objects.get(id=4)
        print(room,'hahaha')
        data = {
            'roomId': room.id,
            'rent': rent,
            'rent_from': rent_from,
            'rent_to': rent_to,
        }
        print(room.id,'dafa')
        room.rented = True
        room.rent_from = rent_from
        room.rent_to = rent_to
        room.save()


        serializer = RentedRoomsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(
                {"success": False, "message": "Invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
    except RoomDetails.DoesNotExist:
        return Response(
            {"success": False, "message": "Room not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print("Error:", str(e))
        return Response(
            {"success": False, "message": "An error occurred on the server."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def create_payment(request):
    user = request.user  # Get the logged-in user
    rent_id = request.data.get("rent_id")
    total_amount = request.data.get("total_amount")
    transaction_uuid = request.data.get("transaction_uuid")
    print('payment',request.data,user,rent_id,total_amount,transaction_uuid)

    try:
        # Validate and fetch the related RoomDetails object
        room = RoomDetails.objects.get(id=rent_id)
    except RoomDetails.DoesNotExist:
        return Response({"error": "Room with the given ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

    # Prepare payment data for serialization
    payment_data = {
        "user": user.id,
        "room": room.id,
        "transaction_uuid": transaction_uuid,
        "amount": Decimal(total_amount),
        "status": "success",
    }

    # Validate and save payment using the serializer
    serializer = PaymentSerializer(data=payment_data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Payment created successfully.", "payment": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
