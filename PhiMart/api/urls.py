from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet
from order.views import CartViewSet, CartItemViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet)
router.register('carts', CartViewSet, basename='carts')
router.register('cart-items', CartItemViewSet, basename='cart-items')

# Nested router for cart items under carts
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', CartItemViewSet, basename='cart-items-nested')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(carts_router.urls)),
]
