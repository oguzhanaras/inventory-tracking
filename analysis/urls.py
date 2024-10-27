# analysis/urls.py
from django.urls import path
from .views import user_analysis


app_name = 'analysis'  # Namespace tanımı

urlpatterns = [
    path('', user_analysis, name='user_analysis'),
]
