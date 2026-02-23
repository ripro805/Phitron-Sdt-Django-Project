from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_categories, name='category-list'),
    path('<int:pk>/', views.view_category_detail, name='category-detail'),
]
