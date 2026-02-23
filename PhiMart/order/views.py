from rest_framework import mixins, viewsets
from order.models import Cart, CartItem, Order, OrderItem
from order.serializers import CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet



class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,  # Enables GET /api/carts/
    viewsets.GenericViewSet
):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(CreateModelMixin):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(CreateModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(CreateModelMixin):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
