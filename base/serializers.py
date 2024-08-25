from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    # name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','username','email']

    # def get_name(self, obj):
    #     name = obj.name
    #     if name == '':
    #         name = obj.email
    #     return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email','token']
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
