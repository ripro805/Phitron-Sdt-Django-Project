from rest_framework import mixins, viewsets
from order.models import Cart, CartItem, Order, OrderItem
from order.serializers import AddCartItemSerializer, UpdateCartItemSerializer, CartItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from rest_framework.permissions import IsAuthenticated

class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,  # Enables GET /api/carts/
    viewsets.GenericViewSet
):
    
    serializer_class = CartSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

class OrderViewSet(viewsets.ModelViewSet):
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
       if self.request.user.is_staff:
           return Order.objects.select_related('product').all()
       return Order.objects.select_related('product').filter(user=self.request.user)

class OrderItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        from order.serializers import AddCartItemSerializer, UpdateCartItemSerializer, CartItemSerializer
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        from order.models import CartItem
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
