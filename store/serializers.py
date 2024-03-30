from rest_framework import serializers

from store.models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'phone', 'birth_date', 'membership']


class MeCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['phone', 'birth_date', 'membership']


class CustomerAddressSerializer(serializers.ModelSerializer):
    zip_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'zip_code']


class CollectionSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    featured_product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'products']


class ProductSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    promotions = serializers.PrimaryKeyRelatedField(
        queryset=Promotion.objects.all(), many=True, allow_empty=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'unit_price', 'inventory', 'collection', 'promotions']


class PromotionSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True, allow_empty=True, required=False)

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


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    @staticmethod
    def get_total_price(cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    def save(self, **kwargs):
        product = self.validated_data['product']
        quantity = self.validated_data['quantity']
        cart = self.context.get('cart')

        try:
            cart_item = CartItem.objects.get(cart_id=cart, product_id=product)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    @staticmethod
    def get_total_price(cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
