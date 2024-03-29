from rest_framework import serializers
from store.models import *
from . import validator


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Customer
        fields = ['user', 'phone', 'birth_date', 'membership']


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title', 'featured_products_id']

    featured_products_id = serializers.ListField(child=serializers.IntegerField(), required=False)

    @staticmethod
    def validate_featured_products_id(value):
        return validator.has_relation(Product, serializers, value, many=True)

