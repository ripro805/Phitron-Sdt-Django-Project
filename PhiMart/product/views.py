
   


from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product

@api_view(['GET'])
def view_products(request):
    products =get_object_or_404(Product,pk=id)
    product_dict = {
        "id": products.id,
        "name": products.name,
        "description": products.description,
        "price": products.price,
        "stock": products.stock,
    }
    return Response({"product": product_dict})

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