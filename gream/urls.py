from django.urls import path, include

from products.views import ProductView, CategoryView

urlpatterns = [
    path('users', include('users.urls')),
    path('orders', include('orders.urls')),
    path('products', include('products.urls'))
]