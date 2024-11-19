from django.contrib.auth import authenticate, get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = (
                     "first_name",
                     "last_name",
                     "profile_picture_url",
                 ) + BaseUserCreateSerializer.Meta.fields


class TokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = get_user_model().objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        user = authenticate(
            request=self.context.get("request"),
            username=user.username,
            password=password
        )
        
        if user is None or not user.is_active:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        print(f"Refresh token: {refresh}")
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "profile_picture_url",
            "gender",
        )
