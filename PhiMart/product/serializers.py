from rest_framework import serializers
from .models import Product, Category
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_with_tax')
    
    def calculate_price_with_tax(self, product):
        return product.price * Decimal('1.1')  # Assuming 10% tax

    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price', 'price_with_tax']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
