from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # add extra field here
    email = models.EmailField(unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['first_name'], name='first_name_idx'),
            models.Index(fields=['last_name'], name='last_name_idx'),
        ]
