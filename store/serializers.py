from rest_framework import serializers

from store.models import *


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Customer
        fields = ['user', 'phone', 'birth_date', 'membership']


class CustomerAddressSerializer(serializers.ModelSerializer):
    zip_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Address
        fields = ['street', 'city', 'zip_code']


class CollectionSerializer(serializers.ModelSerializer):
    featured_product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), allow_null=True,
                                                          required=False)
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'products']


class ProductSerializer(serializers.ModelSerializer):
    promotions = serializers.PrimaryKeyRelatedField(queryset=Promotion.objects.all(), many=True, allow_empty=True,
                                                    required=False)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'unit_price', 'inventory', 'collection', 'promotions']


class PromotionSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, allow_empty=True,
                                                  required=False)

    class Meta:
        model = Promotion
        fields = ['id', 'description', 'discount', 'products']


class ProductPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'description', 'discount']


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'title', 'description']
