import json

from django.utils import timezone

from django.http.response import JsonResponse

from django.db.models import Q
from products.models import Product
from orders.models import Bidding, Contract, Status
from orders.response import orders_schema_dict

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from utils import authorization
from decorators import query_debugger

class BiddingView(APIView):
    @swagger_auto_schema(manual_parameters = [], responses = orders_schema_dict)
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
                is_seller         = False if contract_type =='buy' else True,
                user              = user,
                product_id        = product_id,
                price             = data['price'],
                status_id         = Status.ON_BIDDING
            )

            product = Product.objects.get(id=product_id)

            if contract_type == 'buy' and bidding.price > product.current_selling_price:
                product.current_selling_price = bidding.price

            if contract_type == 'sell' and bidding.price < product.current_buying_price:
                product.current_buying_price = bidding.price
            
            product.save()

            return JsonResponse({'message': 'NEW_BID_CREATED'}, status=201)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class ContractView(APIView):
    @swagger_auto_schema(manual_parameters = [], responses = orders_schema_dict)
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
                if not Bidding.objects.filter(id=selling_bid_id, status_id=Status.ON_BIDDING, is_seller=True, product_id=product_id).exists():
                    return JsonResponse({'message': 'SELLING_BID_NOT_FOUND'}, status=404)
                
                selling_bid = Bidding.objects.get(id=selling_bid_id)

                buying_bid  = Bidding.objects.create(
                    is_seller  = False,
                    user       = user,
                    product_id = product_id,
                    price      = selling_bid.price,
                    status     = Status.ON_BIDDING
                )

            if contract_type == 'sell':
                if not Bidding.objects.filter(id=buying_bid_id, status_id=Status.ON_BIDDING, is_seller=False, product_id=product_id).exists():
                    return JsonResponse({'message': 'BUYING_BID_NOT_FOUND'}, status=404)
                
                buying_bid = Bidding.objects.get(id=buying_bid_id)

                selling_bid  = Bidding.objects.create(
                    is_seller  = True,
                    user       = user,
                    product_id = product_id,
                    price      = buying_bid.price,
                    status     = Status.ON_BIDDING
                )

            Contract.objects.create(
                selling_bid = selling_bid,
                buying_bid  = buying_bid
            )

            buying_bid.status_id  = Status.CONTRACTED
            selling_bid.status_id = Status.CONTRACTED
            buying_bid.save()
            selling_bid.save()

            return JsonResponse({'message': 'CONTRACT_SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': "KEY_ERROR"}, status=400)

class BiddinghistoryView(APIView):
    @swagger_auto_schema(manual_parameters = [], responses = orders_schema_dict)
    @authorization
    @query_debugger
    def get(self, request):
        status_id = request.GET.get("status_id", None)
        offset    = int(request.GET.get("offset", 0))
        limit     = int(request.GET.get("limit", 100))
        offset    = offset * limit
        limit     = offset + limit
        
        q = Q()

        if status_id:
            q &= Q(status_id=status_id)
         
        biddings = Bidding.objects.select_related('product', 'status').filter(q)[offset:limit]

        biddinglist = [
            {
                "product_id"    : bidding.product.id,
                "product_name"  : bidding.product.name,
                "is_seller"     : bidding.is_seller,
                "image"         : bidding.product.productimage_set.first().image_url,
                "status_id"     : bidding.status.id,
                "status_name"   : bidding.status.name,
                "price"         : bidding.price,
                "bidding_date"  : bidding.updated_at.strftime("%Y.%m.%d"),
                "expired_date"  : (bidding.updated_at + timezone.timedelta(days=bidding.expired_within.period)).strftime("%Y.%m.%d"),
            } for bidding in biddings
        ]
        return JsonResponse({"results": biddinglist}, status = 200)