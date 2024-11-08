from django.contrib.auth import authenticate, get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('first_name', 'last_name', 'profile_picture_url') + BaseUserCreateSerializer.Meta.fields


class TokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(request=self.context.get("request"), username=email, password=password)

        if user is None:
            user = get_user_model().objects.filter(email=email).first()
            if user and not user.check_password(password):
                raise serializers.ValidationError("Invalid credentials")

        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        raise serializers.ValidationError("Invalid credentials")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "username", "first_name", "last_name", "profile_picture_url")
