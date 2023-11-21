from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
class User(AbstractUser):
    username = models.EmailField(unique=True, null=True)
    linkedin_info = models.TextField()
    linkedin_url = models.URLField()
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(default=False,null=True)
    is_active = models.BooleanField(default=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username