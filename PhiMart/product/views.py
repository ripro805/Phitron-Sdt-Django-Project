
   


from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer
@api_view()
def view_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response({"products": serializer.data})

@api_view(['GET'])
def view_product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response({"product": serializer.data})
@api_view(['GET'])
def view_categories(request):
    c = get_object_or_404(Category,pk=id)
    data = [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
        }
        
    ]
    
    return Response({"categories": data})