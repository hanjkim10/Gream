from django.urls import path

from orders.views import BiddingView, ContractView, BiddinghistoryView

urlpatterns = [
    path('/bidding', BiddingView.as_view()),
    path('/contract', ContractView.as_view()),
    path('/bidding', BiddinghistoryView.as_view())
]
