# sales/urls.py
from django.urls import path
from .views import create_sale, sale_list

app_name = 'sales'  # Namespace tanımı

urlpatterns = [
    path('', sale_list, name='sale_list'),
    path('create/', create_sale, name='create_sale'),
]
