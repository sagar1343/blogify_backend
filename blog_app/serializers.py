from unicodedata import category

from rest_framework import serializers
from rest_framework.serializers import Serializer

from .models import Blog, Category


class CategorySerializer(serializers.ModelSerializer):
    blog_count = blog_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'blog_count']


class BlogSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'content', 'category', 'read_by', 'date', 'author']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if 'category' in representation:
            category_instance = instance.category
            category_data = CategorySerializer(category_instance).data
            representation['category'] = category_data
        return representation
