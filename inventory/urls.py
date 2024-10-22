from django.urls import path
from . import views

app_name = 'inventory'  # Namespace tanımlaması

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product, name='product'),
    path('product/create/', views.create_product, name='create_product'),
    path('product/detail/<int:id>/', views.view_product, name='view_product'),
    path('product/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:id>/', views.delete_product, name='delete_product'),
]