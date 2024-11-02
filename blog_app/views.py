from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Blog, Category
from .serializers import BlogSerializer, CategorySerializer


class BlogView(ListCreateAPIView):
    queryset = Blog.objects.all().select_related('category').order_by('title')
    serializer_class = BlogSerializer

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



class CategoryView(ListCreateAPIView):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    pagination_class = None
