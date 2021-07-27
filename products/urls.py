from django.urls import path

from products.views import ProductView, CategoryView, ProductDetailView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]
