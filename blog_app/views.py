from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Blog, Category
from .serializers import BlogSerializer, CategorySerializer, UsersBlogSerializer


class BlogView(ListCreateAPIView):
    queryset = Blog.objects.all().select_related('category', 'author').order_by('-date')
    serializer_class = BlogSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'category']
    search_fields = ['title']
    ordering_fields = ['title', 'read_by', 'date']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        else:
            return [AllowAny()]


class BlogDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.read_by += 1
        instance.save(update_fields=['read_by'])
        return super().get(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]


class UsersBlogView(ListAPIView):
    serializer_class = UsersBlogSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user).only('title', 'read_by')


class CategoryView(ListCreateAPIView):
    queryset = (Category.objects.all()
                .prefetch_related('blog_set')
                .annotate(blog_count=Count('blog'))
                .order_by('-blog_count'))
    serializer_class = CategorySerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    pagination_class = None

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response_data = {
            'count': self.queryset.count(),
            'results': response.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
