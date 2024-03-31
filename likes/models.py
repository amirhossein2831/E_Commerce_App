from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.models import User


class LikedItemManager(models.Manager):

    @staticmethod
    def get_like_for(content_type, object_id):
        content_type = ContentType.objects.get_for_model(content_type)

        return LikedItem.objects.filter(
            content_type=content_type,
            object_id=object_id
        )


class LikedItem(models.Model):
    objects = LikedItemManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='likes')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
