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


class CartItemViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def list(self, request, *args, **kwargs):
        cart_pk = self.kwargs.get('cart_pk')
        if cart_pk:
            self.queryset = self.queryset.filter(cart_id=cart_pk)
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        cart_pk = self.kwargs.get('cart_pk')
        if cart_pk:
            serializer.save(cart_id=cart_pk)
        else:
            serializer.save()

class OrderViewSet(CreateModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(CreateModelMixin):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
