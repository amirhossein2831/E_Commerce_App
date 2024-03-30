from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import serializers
from .models import Customer, Collection, Product, Promotion, Review, Address, Cart
from .permissoin import IsAuthAdminUserOrAuthReadOnly


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return serializers.MeCustomerSerializer
        if self.request.method == 'PUT':
            return serializers.MeCustomerSerializer
        return serializers.CustomerSerializer

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request: Request) -> Response:
        customer = get_object_or_404(Customer, user=request.user)
        if request.method == 'GET':
            serializer = serializers.MeCustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = serializers.MeCustomerSerializer(customer, request.data)
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
        return Address.objects.filter(customer=self.kwargs['customers_pk'])

    def perform_create(self, serializer):
        serializer.save(customer=Customer(pk=self.kwargs['customers_pk']))


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.prefetch_related('products').all()
    serializer_class = serializers.CollectionSerializer
    permission_classes = [IsAuthAdminUserOrAuthReadOnly]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('promotions').all()
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
        return Review.objects.filter(product=self.kwargs['products_pk'])

    def perform_create(self, serializer):
        serializer.save(product=Product(pk=self.kwargs['products_pk']))


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializer
