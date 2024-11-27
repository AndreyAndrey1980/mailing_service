from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [email]

    class Meta:
        permissions = [
            ("manager_permissions", "See all users and mailing, can block user, can stop mailing"),
        ]
