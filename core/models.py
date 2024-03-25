from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    # add extra field here
    email = models.EmailField(unique=True)
