from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import *


urlpatterns = [
    # Users
    path('user/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/profile/', getUserProfile, name='users'),
    path('user/type/', getUserType, name='usersProfile'),
    path('user/register/', registerUser, name='registerUsers'),
    path('user/login/', MyTokenObtainPairView.as_view(), name='login'),


    # Registration Details
    path('registrationdetails/', getRegistrationDetails, name='registrationDetails'),

    # Chat Messages
    path('myMessages/<user_id>/', MyInbox.as_view(), name='messageList'),
    path('getMessages/<sender_id>/<receiver_id>/', GetMessages.as_view(), name='messages'),
    path('sendMessages/', SendMessage.as_view(), name='sendMessages'),
    
    # Get Profile
    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profileDetail'),
    path('search/<username>/', SearchUser.as_view(), name='searchUser'),
]

