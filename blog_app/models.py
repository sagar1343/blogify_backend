from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255)
    content = models.TextField()
    read_by = models.PositiveIntegerField(default=0, editable=False)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
