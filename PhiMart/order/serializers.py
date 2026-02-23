from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from users.models import User
from product.serializers import ProductSerializer

class UserDropDownField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        # Only users without a cart
        return User.objects.filter(cart__isnull=True)
    def display_value(self, instance):
        return instance.email



    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']
    def validate_user(self, value):
        if Cart.objects.filter(user=value).exists():
            raise serializers.ValidationError("This user already has a cart.")
        return value

class CartItemSerializer(serializers.ModelSerializer):
    product_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product_price', 'quantity']

    def get_product_price(self, obj):
        return obj.product.price if obj.product else None
class CartSerializer(serializers.ModelSerializer):
    user = UserDropDownField(queryset=User.objects.all())
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(
            (item.product.price if item.product else 0) * item.quantity
            for item in obj.items.all()
        )

    def validate_user(self, value):
        if Cart.objects.filter(user=value).exists():
            raise serializers.ValidationError("This user already has a cart.")
        return value
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
