from rest_framework import serializers
from .models import Product, Category, Review
from decimal import Decimal

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=200)
#     unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='price')
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_with_tax')
#     # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     # category=serializers.StringRelatedField()  # Use the __str__ method of Category for representation
#     category=serializers.HyperlinkedRelatedField(view_name='category-detail', read_only=True)  # Hyperlinked representation 
#     def calculate_price_with_tax(self, product):
#         return product.price * Decimal('1.1')  # Assuming 10% tax

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']

class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_with_tax')
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'category', 'price_with_tax']

    def calculate_price_with_tax(self, product):
        return product.price * Decimal('1.1')  # Assuming 10% tax

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters.")
        return value

    # def validate(self, attrs):
    #     price = attrs.get('price', 0)
    #     stock = attrs.get('stock', 0)
    #     if price > 10000 and stock > 100:
    #         raise serializers.ValidationError("If price is very high, stock should not exceed 100.")
    #     return attrs

    # def create(self, validated_data):
    #     category_id = self.initial_data.get('category')
    #     category = None
    #     if category_id:
    #         category = Category.objects.get(pk=category_id)
    #     product = Product.objects.create(
    #         name=validated_data['name'],
    #         description=validated_data.get('description', ''),
    #         price=validated_data['price'],
    #         stock=validated_data['stock'],
    #         image=validated_data.get('image', None),
    #         category=category
    #     )
    #     return product
    

class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = Review
        fields = ['id', 'product', 'name', 'description', 'date']
        def create(self, validated_data):
            product_id = self.context.get('product_id')
            return Review.objects.create(product_id=product_id, **validated_data)