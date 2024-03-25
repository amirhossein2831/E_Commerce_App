from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # add extra field here
    email = models.EmailField(unique=True)


class AuditableModelManager(models.Manager):
    def create(self, user=None, **kwargs):
        if user is not None:
            kwargs.setdefault('created_by', user)
        return super().create(**kwargs)

    def update(self, user=None, **kwargs):
        if user is not None:
            kwargs['updated_by'] = user
        return super().update(**kwargs)


class AuditableModel(models.Model):
    class Meta:
        abstract = True

    objects = AuditableModelManager()

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, primary_key=True)

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, primary_key=True)

    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, primary_key=True)

    def save(self, user=None, *args, **kwargs):
        if user is not None:
            if not self.pk:
                self.created_by = user
            self.updated_by = user
        super().save(*args, **kwargs)
