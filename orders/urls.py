from django.urls import path

from orders.views import BiddingView, ContractView

urlpatterns = [
    path('/bidding', BiddingView.as_view()),
    path('/contract', ContractView.as_view()),
]