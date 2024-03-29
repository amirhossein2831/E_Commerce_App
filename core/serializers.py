from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_superuser', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        staff = self.context["request"].user.is_staff
        superuser = self.context["request"].user.is_superuser

        if not staff and not superuser:
            self.fields.pop('is_staff')
            self.fields.pop('is_superuser')
        elif staff and not superuser:
            self.fields.pop('is_superuser')


class UserSerializer(BaseUserSerializer):
    is_staff = serializers.BooleanField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']
