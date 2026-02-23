
   


from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)
    

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer
