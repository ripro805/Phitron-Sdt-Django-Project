from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_products, name='product-list'),
    path('<int:pk>/', views.view_product_detail, name='product-detail'),
]
