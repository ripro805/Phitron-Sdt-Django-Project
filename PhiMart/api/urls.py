from django.urls import path, include
from . import views
from product.views import view_categories

urlpatterns = [
    path('', views.api_home, name='api_home'),
    path('products/', include('product.product_urls')),
    path('users/', include('users.urls')),
    path('orders/', include('order.urls')),
    path('categories/', include('product.categories_urls')),
]
