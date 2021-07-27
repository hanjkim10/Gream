import json

from django.views       import View
from django.utils       import timezone

from django.http.response import JsonResponse

from django.db.models   import Q
from products.models    import Product
from orders.models      import Bidding, Contract, Status
from utils              import authorization

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
                # 상세페이지에서 넘어온 판매입찰건의 id를 가지고, status가 '입찰중'이고, is_seller=1(판매입찰건 / 'is_seller=0': 구매입찰)이고, 해당 제품id와 같은 id를 갖는 bidding이 존재하지 않을경우,
                # 'SELLING_BID_NOT_FOUND' 에러 발생
                if not Bidding.objects.filter(id=selling_bid_id, status_id=1, is_seller=1, product_id=product_id).exists():
                    return JsonResponse({'message': 'SELLING_BID_NOT_FOUND'}, status=404)
                
                # 위에 filter한 객체가 존재할 경우, 'selling_bid'라는 변수로 받아두고
                selling_bid = Bidding.objects.get(id=selling_bid_id)

                # 즉시구매를 체결할 경우, 현재 유저가 구매하고자 하는 상품에 대한 구매입찰이 등록되지 않은 상태이므로, 체결 전에 구매입찰 등록
                buying_bid  = Bidding.objects.create(
                    is_seller  = 0,
                    user       = user,
                    product_id = product_id,
                    price      = selling_bid.price,
                    status     = Status.objects.get(id=1)
                )

            # 구매 > 판매로 바뀌고, 나머지 내용은 위와 같음
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

            # 판매의 경우, 위에서 생성한 selling_bid와 상세페이지에서 넘어온 buying_bid를 받아와 둘의 체결 등록
            Contract.objects.create(
                selling_bid = selling_bid,
                buying_bid  = buying_bid
            )

            # 체결등록 후, 각 입찰건의 입찰상태를 status_id=3(체결완료)로 변경
            buying_bid.status_id = 3
            selling_bid.status_id = 3
            buying_bid.save()
            selling_bid.save()

            return JsonResponse({'message': 'CONTRACT_SUCCESS'}, status=201)

        # except문으로는 KeyError만 처리, 나머지 발생할 수 있는 에러들은 위에서 if문으로 처리
        except KeyError:
            return JsonResponse({'message': "KEY_ERROR"}, status=400)


class BiddinghistoryView(View):
    def get(self, request):
        status_id = request.GET.get("status_id", None)
        offset    = int(request.GET.get("offset",0))
        limit     = int(request.GET.get("limit",100))
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
        return JsonResponse({"results":biddinglist}, status = 200)