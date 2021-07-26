from orders.views import ContractView
from django.urls import path

urlpatterns = [
    path('/contract', ContractView.as_view()),
]