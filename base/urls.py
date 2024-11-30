from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'chat-messages', ChatMessageViewSet, basename='chatmessage')


urlpatterns = [
    # Users
    path('user/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/profile/', getUserProfile, name='users'),
    path('user/type/', getUserType, name='usersProfile'),
    path('user/register/', registerUser, name='registerUsers'),
    path('user/list/', userList, name='userList'),
    path('user/login/', MyTokenObtainPairView.as_view(), name='login'),


    # Registration Details
    path('registrationdetails/', getRegistrationDetails, name='registrationDetails'),
    path('user/verify/', verify_user, name='verifyUser'),

    # Chat Messages
    path('', include(router.urls)),
    path('chat-users/', get_chat_users, name='get-chat-users'),
    # path('sendMessages/', SendMessage.as_view(), name='sendMessages'),
    # path('myMessages/<user_id>/', MyInbox.as_view(), name='messageList'),
    # path('getMessages/<sender_id>/<receiver_id>/', GetMessages.as_view(), name='messages'),
    # path('sendMessages/', SendMessage.as_view(), name='sendMessages'),
    
    # Get Profile
    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profileDetail'),
    path('search/<username>/', SearchUser.as_view(), name='searchUser'),

    # Room Details
    path('roomdetails/', room_details, name='roomDetails'),
    path('roomdetail/', room_detail, name='roomDetail'),
    path('addrooms/', add_rooms, name='addRoom'),
    path('handle-rent/', handle_rent, name='handle_rent'),


    path('toggle-verify-user/<int:user_id>/', toggle_verify_user, name='toggle_verify_user'),



]

