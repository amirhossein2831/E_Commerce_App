from rest_framework import serializers

from store.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['user_id', 'phone', 'birth_date', 'membership']

