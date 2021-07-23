from django.urls import path

from products.views import ProductView, CategoryView

urlpatterns = [
    path ('', ProductView.as_view()),
    path ('/category', CategoryView.as_view())
]
