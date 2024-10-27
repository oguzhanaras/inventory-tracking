from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls', namespace='inventory')),
    path('category/', include('category.urls', namespace='category')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('users/', include('users.urls', namespace='users')),
    path('sale/', include('sale.urls', namespace='sale')),
    path('analysis/', include('analysis.urls')),
]
