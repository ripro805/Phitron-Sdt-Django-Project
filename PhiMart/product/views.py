
   
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category

@api_view(['GET'])
def view_products(request):
    # For demonstration, we'll return a static list of products.
    products = [
        {"id": 1, "name": "Product A", "price": 10.99},
        {"id": 2, "name": "Product B", "price": 15.99},
        {"id": 3, "name": "Product C", "price": 7.99},
    ]
    return Response(products)
@api_view(['GET'])
def view_categories(request):
     categories = Category.objects.all()
     data = [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
        }
        for c in categories
    ]
     return Response({"categories": data})