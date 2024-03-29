from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import serializers
from .models import Customer, Collection
from .permissoin import IsAuthAdminUserOrAuthReadOnly


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request: Request) -> Response:
        customer = get_object_or_404(Customer, user=request.user)
        if request.method == 'GET':
            serializer = serializers.CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = serializers.CustomerSerializer(customer, request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = serializers.CollectionSerializer
    permission_classes = [IsAuthAdminUserOrAuthReadOnly]

