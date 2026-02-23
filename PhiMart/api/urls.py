
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from  rest_framework_nested import routers
from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet,basename='products')
router.register('categories', CategoryViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')


urlpatterns = [
    path('', views.api_home, name='api-home'),
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
