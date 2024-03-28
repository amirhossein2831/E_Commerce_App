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
        fields = ['title', 'featured_products_id']

    featured_products_id = serializers.ListField(child=serializers.IntegerField())

    def validate_featured_products_id(self, value):
        for product_id in value:
            if not Product.objects.filter(pk=product_id).exists():
                raise serializers.ValidationError(f"Product with ID {product_id} does not exist.")
        return value