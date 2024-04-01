from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from . import serializers
from .models import *
from .permissoin import IsAuthAdminUserOrAuthReadOnly


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['head', 'options', 'get', 'put', 'patch', 'delete']

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request: Request) -> Response:
        customer = get_object_or_404(Customer, user=request.user)
        if request.method == 'GET':
            serializer = serializers.CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = serializers.CustomerSerializer(customer, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class LoginCustomerAddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = serializers.CustomerAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(customer_id=self.request.user.id).all()

    def perform_create(self, serializer):
        serializer.save(customer_id=self.request.user.id)


class CustomerAddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = serializers.CustomerAddressSerializer
    permission_classes = [IsAuthAdminUserOrAuthReadOnly]

    def get_queryset(self):
        return Address.objects.filter(customer=self.kwargs['customers_pk']).all()

    def perform_create(self, serializer):
        serializer.save(customer=Customer(pk=self.kwargs['customers_pk']))


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.prefetch_related('products').all()
    serializer_class = serializers.CollectionSerializer
    permission_classes = [IsAuthAdminUserOrAuthReadOnly]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('promotions', 'images').all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthAdminUserOrAuthReadOnly]


class PromotionViewSet(ModelViewSet):
    queryset = Promotion.objects.prefetch_related('products').all()
    serializer_class = serializers.PromotionSerializer
    permission_classes = [IsAuthAdminUserOrAuthReadOnly]


class ProductPromotionViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = serializers.ProductPromotionSerializer
    permission_classes = [IsAuthAdminUserOrAuthReadOnly]

    def get_queryset(self):
        return Promotion.objects.filter(products=self.kwargs['products_pk'])

    def perform_create(self, serializer):
        serializer.save(products=[self.kwargs['products_pk']])


class ProductReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ProductReviewSerializer
    permission_classes = [IsAuthAdminUserOrAuthReadOnly]

    def get_queryset(self):
        return Review.objects.filter(product=self.kwargs['products_pk']).all()

    def perform_create(self, serializer):
        serializer.save(product=Product(pk=self.kwargs['products_pk']))


class CartViewSet(DestroyModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items', 'items__product', 'items__product__promotions').all()
    serializer_class = serializers.CartSerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    http_method_names = ['head', 'options', 'get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.kwargs['carts_pk']).select_related('product').all()

    def get_serializer_context(self):
        return {'cart': self.kwargs['carts_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddCartItemSerializer
        if self.request.method in ['PATCH']:
            return serializers.UpdateCartSerializer
        return serializers.CartItemSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    http_method_names = ['head', 'options', 'get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return (Order.objects.
                    prefetch_related('items', 'items__product', 'items__product__promotions').all())
        return (Order.objects.filter(customer_id=self.request.user.id).
                prefetch_related('items', 'items__product', 'items__product__promotions').all())

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return serializers.UpdateOrderSerializer
        return serializers.OrderSerializer

    def get_serializer_context(self, **kwargs):
        return {'user': self.request.user}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = serializers.OrderSerializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product=self.kwargs['products_pk']).all()

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs['products_pk'])
