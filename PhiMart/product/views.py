
   


from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer
from django.db.models import Count


@api_view(['GET', 'POST'])
def view_products(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    else:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({"products": serializer.data})
      

@api_view(['GET', 'PUT', 'DELETE'])
def view_product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response({"product": serializer.data})
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        copy_of_product = Product.objects.get(pk=pk)  # Get a copy of the product before deletion
        serializer=ProductSerializer(copy_of_product, context={'request': request})  # Serialize the copy
        product.delete()
        return Response(status=204)
    
@api_view(['GET', 'POST'])
def view_categories(request):
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    categories = Category.objects.annotate(product_count=Count('products')).all()
    serializer = CategorySerializer(categories, many=True)
    return Response({"categories": serializer.data})

@api_view(['GET'])
def view_category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response({"category": serializer.data})