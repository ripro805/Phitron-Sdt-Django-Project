
   


from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

class ViewProduct(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({"products": serializer.data})

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
      

class ProductDetailsView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response({"product": serializer.data})

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=204)
    

class ViewCategory(APIView):
    def get(self, request):
        categories = Category.objects.annotate(product_count=Count('products')).all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"categories": serializer.data})

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class CategoryDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response({"category": serializer.data})

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=204)
    
    
class ProductListView(ListAPIView):
    queryset=Product.objects.select_related('category').all()
    serializer_class=ProductSerializer
    
    # def get_queryset(self):
    #     return Product.objects.select_related('category').all()
    # def get_serializer_class(self):
    #     return ProductSerializer
    
    # def get_serializer_context(self):
    #     return {'request': self.request}

class CategoryListView(ListAPIView):
    queryset=Category.objects.annotate(product_count=Count('products')).all()
    serializer_class=CategorySerializer

class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.select_related('category').all()
    serializer_class=ProductSerializer
    lookup_field='pk'
    
class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'
    