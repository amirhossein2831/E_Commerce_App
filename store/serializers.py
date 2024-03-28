from rest_framework import serializers
from store.models import *


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Customer
        fields = ['user', 'phone', 'birth_date', 'membership']



class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
