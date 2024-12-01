from .models import Comment
from .serializers import CommentSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class CommentView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        if self.request and self.request.method == "GET":
            return Comment.objects.filter(object_id=self.kwargs.get("pk")).order_by("-commented_at")
        return super().get_queryset()
