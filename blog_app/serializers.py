from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Blog, Category


class CategorySerializer(serializers.ModelSerializer):
    blog_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "title", "blog_count"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_picture_url",
        ]


class BlogSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "description",
            "content",
            "category",
            "read_by",
            "upvote",
            "date",
            "author",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if "author" in representation:
            author_instance = instance.author
            representation["author"] = AuthorSerializer(author_instance).data

        if "category" in representation:
            category_instance = instance.category
            representation["category"] = CategorySerializer(category_instance).data

        return representation


class UsersBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "read_by"]
