from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.models import User


# Create your models here.
class LikeItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='likes')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()