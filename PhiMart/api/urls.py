
from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from product.views import ProductViewSet, CategoryViewSet

router = SimpleRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
urlpatterns = router.urls