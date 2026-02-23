from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from users.models import User

class UserDropDownField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        # Only users without a cart
        return User.objects.filter(cart__isnull=True)
    def display_value(self, instance):
        return instance.email

class CartSerializer(serializers.ModelSerializer):
    user = UserDropDownField(queryset=User.objects.all())
    class Meta:
        model = Cart
        fields = '__all__'
    def validate_user(self, value):
        if Cart.objects.filter(user=value).exists():
            raise serializers.ValidationError("This user already has a cart.")
        return value

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
