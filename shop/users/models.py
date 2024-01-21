from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='email address')
    username = models.CharField(unique=False, max_length=99)

    purchases = models.IntegerField(default=0)
    is_associate = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
