from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )

    is_email_verified = models.BooleanField(default=False)

    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name or self.user.username
