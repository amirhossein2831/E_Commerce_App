from rest_framework import serializers

from store.models import *


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Customer
        fields = ['user', 'phone', 'birth_date', 'membership']


class CollectionSerializer(serializers.ModelSerializer):
    featured_product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), allow_null=True,
                                                          required=False)
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['title', 'featured_product', 'products']


class ProductSerializer(serializers.ModelSerializer):
    promotions = serializers.PrimaryKeyRelatedField(queryset=Promotion.objects.all(), many=True, allow_empty=True,
                                                    required=False)

    class Meta:
        model = Product
        fields = ['title', 'description', 'unit_price', 'inventory', 'collection', 'promotions']
