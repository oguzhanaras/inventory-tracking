from django.urls import path
from . import views


app_name = 'category'

urlpatterns = [
    path('', views.category_list, name='list'),
    path('create/', views.category_create, name='create'),
    path('detail/<int:id>/', views.view_category, name='detail'),
    path('update/<int:id>/', views.category_update, name='update'),
    path('delete/<int:id>/', views.category_delete, name='delete'),
]