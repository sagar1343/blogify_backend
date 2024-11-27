from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model


# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    comment = models.TextField()
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
