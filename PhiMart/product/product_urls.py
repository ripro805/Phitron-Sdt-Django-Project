from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_products, name='product-list'),
]
