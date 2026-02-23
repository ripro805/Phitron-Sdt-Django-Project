from rest_framework.response import Response
from .models import Category, Product, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .paginations import DefaultPagination
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['category_id']
    filterset_class = ProductFilter
    search_fields = ['name', 'description','category__name']
    ordering_fields = ['price', 'created_at']
    pagination_class = DefaultPagination
 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)
    

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    def get_query_set(self):
        product_id = self.kwargs.get('product_pk')
        return Review.objects.filter(product_id=product_id)
    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}