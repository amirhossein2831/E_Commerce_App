from rest_framework import serializers
from django.db import transaction
from store.models import *


class CustomerSerializer(serializers.ModelSerializer):
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


class UpdateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


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


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    placed_at = serializers.DateTimeField(source='created_at')
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'payment_status', 'placed_at', 'items']


class CreateOrderSerializer(serializers.Serializer):
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())

    @staticmethod
    def validate_cart(value):
        if CartItem.objects.filter(cart=value).count() == 0:
            raise serializers.ValidationError('the cart is empty')

    @transaction.atomic
    def save(self, **kwargs):
        cart = self.validated_data['cart']
        customer = Customer.objects.get(user=self.context.get('user'))
        order = Order.objects.create(customer=customer)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')

        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.unit_price
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)
        cart.delete()

        return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
