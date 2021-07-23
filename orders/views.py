import json

from django.views         import View
from django.http.response import JsonResponse

from products.models import Product
from orders.models   import Bidding, Contract, Status
from utils           import authorization

class BiddingView(View):
    @authorization
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            product_id = data['product_id']

            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message': 'PRODUCT_NOT_FOUND'}, status=404)

            contract_type = request.GET.get('type', None)

            if contract_type not in ['buy', 'sell']:
                    return JsonResponse({'message': 'INVALID_TYPE'}, status=400)

            bidding = Bidding.objects.create(
                expired_within_id = data['expired_within_id'],
                is_seller         = 0 if contract_type=='buy' else 1,
                user              = user,
                product_id        = product_id,
                price             = data['price'],
                status_id         = 1 
            )

            product = Product.objects.get(id=product_id)

            if contract_type == 'buy':
                current_selling_price = bidding.price\
                    if bidding.price > product.current_selling_price else product.current_selling_price
                product.current_selling_price = current_selling_price

            else:
                current_buying_price = bidding.price\
                    if bidding.price < product.current_buying_price else product.current_buying_price                
                product.current_buying_price = current_buying_price
            
            product.save()

            return JsonResponse({'message': 'NEW_BID_CREATED'}, status=201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class ContractView(View):
    @authorization
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            contract_type = request.GET.get('type', None)

            if contract_type not in ['buy', 'sell']:
                return JsonResponse({'message': 'INVALID_TYPE'}, status=400)
                    
            product_id     = data['product_id']
            selling_bid_id = data['selling_bid_id']
            buying_bid_id  = data['buying_bid_id']

            if contract_type == 'buy':
                if not Bidding.objects.filter(id=selling_bid_id, status_id=1, is_seller=1, product_id=product_id).exists():
                    return JsonResponse({'message': 'SELLING_BID_NOT_FOUND'}, status=404)
                
                selling_bid = Bidding.objects.get(id=selling_bid_id)

                buying_bid  = Bidding.objects.create(
                    is_seller  = 0,
                    user       = user,
                    product_id = product_id,
                    price      = selling_bid.price,
                    status     = Status.objects.get(id=1)
                )

            if contract_type == 'sell':
                if not Bidding.objects.filter(id=buying_bid_id).exists():
                    return JsonResponse({'message': 'BUYING_BID_NOT_FOUND'}, status=404)
                
                buying_bid = Bidding.objects.get(id=buying_bid_id)

                selling_bid  = Bidding.objects.create(
                    is_seller  = 1,
                    user       = user,
                    product_id = product_id,
                    price      = buying_bid.price,
                    status     = Status.objects.get(id=1)
                )

            Contract.objects.create(
                selling_bid = selling_bid,
                buying_bid  = buying_bid
            )

            buying_bid.status_id = 3
            selling_bid.status_id = 3
            buying_bid.save()
            selling_bid.save()

            return JsonResponse({'message': 'CONTRACT_SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': "KEY_ERROR"}, status=400)