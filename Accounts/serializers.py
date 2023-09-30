from rest_framework import serializers
from Accounts.models import UserAccounts


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccounts
        fields = ("fullname", "username", "email", "password", "user_type")


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class LinkSerializer(serializers.Serializer):
    title = serializers.CharField()
    address = serializers.CharField()