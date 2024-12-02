from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from blog_app.models import Blog
from upvote.models import Upvote


# Create your views here.

class UpvoteView(APIView):
    content_type = ContentType.objects.get_for_model(Blog)
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        upvote, created = Upvote.objects.get_or_create(object_id=pk, content_type=self.content_type, user=request.user)
        if created:
            blog.upvote += 1
            blog.save()
            return Response({"message": "Upvote added"}, status=HTTP_200_OK)
        else:
            upvote.delete()
            blog.upvote -= 1
            blog.save()
            return Response({"message": "Upvote removed"}, status=HTTP_200_OK)

    def get(self, request, pk):
        try:
            has_upvoted = Upvote.objects.filter(object_id=pk,
                                                content_type=self.content_type,
                                                user=request.user).exists()
            return Response({"has_upvoted": has_upvoted}, status=HTTP_200_OK)
        except:
            return Response({"has_upvoted": False}, status=HTTP_200_OK)
