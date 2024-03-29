from rest_framework import serializers
from store.models import *
from . import validator


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Customer
        fields = ['user', 'phone', 'birth_date', 'membership']


class CollectionSerializer(serializers.ModelSerializer):
    featured_product_id = serializers.IntegerField(required=False)
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['title', 'featured_product_id', 'products']

    @staticmethod
    def validate_featured_product_id(value):
        return validator.has_relation(Product, serializers, value)
