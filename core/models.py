from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=150, validators=[MinLengthValidator(3)])
    last_name = models.CharField(max_length=150, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    profile_picture_url = models.URLField(blank=True, null=True)
