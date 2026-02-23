from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_root_view(request):
    # Optionally, you can return a JSON response with API links
    return JsonResponse({
        "message": "Welcome to the PhiMart API Root!",
        "products": "/api/products/",
        "categories": "/api/categories/",
        "carts": "/api/carts/",
        "cart-items": "/api/cart-items/",
        "reviews": "/api/products/<product_id>/reviews/"
    })
