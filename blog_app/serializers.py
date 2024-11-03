from rest_framework import serializers

from .models import Blog, Category


class CategorySerializer(serializers.ModelSerializer):
    blog_count = blog_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'blog_count']


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'content', 'category', 'read_by', 'date', 'author']
