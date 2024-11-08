from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Blog, Category


class CategorySerializer(serializers.ModelSerializer):
    blog_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'blog_count']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture_url']


class BlogSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'content', 'category', 'read_by', 'date', 'author']

    def get_author(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            serializer = AuthorSerializer(obj.author)
            return serializer.data
        return obj.author.id

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if 'category' in representation:
            category_instance = instance.category
            category_data = CategorySerializer(category_instance).data
            representation['category'] = category_data
        return representation
