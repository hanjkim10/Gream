from django.urls import path

from products.views import ProductView, CategoryView, BestAuthorView,ProductDetailView

urlpatterns = [
    path('/bestauthor', BestAuthorView.as_view()),
    path('', ProductView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view())
]
