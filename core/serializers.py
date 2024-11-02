from rest_framework import serializers

from .models import User


class UserCreationSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'profile_picture_url', 'password',
                  'confirmed_password']

    def create(self, validated_data):
        confirmed_password = validated_data.pop('confirmed_password', None)
        if validated_data['password'] != confirmed_password:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'profile_picture_url', 'password']
        extra_kwargs = {'password': {'read_only': True}, 'email': {'read_only': True}}

