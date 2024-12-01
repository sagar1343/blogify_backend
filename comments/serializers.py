from rest_framework import serializers
from core.serializers import UserSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "comment", "object_id", "content_type", "user", "commented_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = UserSerializer(instance.user).data
        return representation
