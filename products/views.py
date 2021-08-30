import json
from datetime                    import datetime, timedelta
from dateutil.relativedelta      import relativedelta

from django.http                 import JsonResponse
from django.views                import View
from django.db.models            import Q, Prefetch, Count
from django.db.models.aggregates import Max
from django.utils                import timezone

from decorators   import query_debugger

from products.models             import Author, Theme, Color, Size, Product, ProductColor, ProductImage
from orders.models               import Bidding, Contract

class BestAuthorView(View):
    @query_debugger
    def get (self, request):
        biddings = Count('product__bidding', filter=Q(product__bidding__is_seller=0))
        popular_biddings = Author.objects.annotate(product_count = biddings).order_by('-product_count')[:4]
        results = [
            {
                "top_author" : topauthor.name,
                "author_id"  : topauthor.id
            } for topauthor in popular_biddings
        ]

        return JsonResponse ({"results":results}, status = 200)

class CategoryView(View):
    @query_debugger
    def get(self, request):
        authors  = Author.objects.all()
        themes   = Theme.objects.all()
        colors   = Color.objects.all()
        sizes    = Size.objects.all()
        results = [
            {
                "category_name"   : "author",
                "category_name_kr": "작가",
                "option"          : [
                    {
                        "name": author.name,
                        "id"  : author.id
                    } for author in authors
                ]},
            {
                "category_name"   : "theme",
                "category_name_kr": "테마",
                "option"          : [
                    {
                        "name": theme.name,
                        "id"  : theme.id
                    } for theme in themes
                ]},
            {
                "category_name"   : "color",
                "category_name_kr": "색상",
                "option"          : [
                    {
                        "name": color.name,
                        "id"  : color.id
                    } for color in colors
                ]},
            {
                "category_name"   : "size",
                "category_name_kr": "크기",
                "option"          : [
                    {
                        "name": size.name,
                        "id"  : size.id
                    } for size in sizes
                ]}
        ]
        return JsonResponse ({"results":results}, status = 200)

class ProductView(View):
    @query_debugger
    def get(self, request):
        author_id = request.GET.getlist("author", None)
        theme_id  = request.GET.getlist("theme", None)
        color_id  = request.GET.getlist("color", None)
        size_id   = request.GET.getlist("size", None)
        sort      = request.GET.get("sort", "original-price-ascending")
        offset    = int(request.GET.get("offset",0))
        limit     = int(request.GET.get("limit",100))
        limit     = offset + limit
        options   = {
            "selling-price-descending" : "-current_selling_price",
            "buying-price-ascending"   : "current_buying_price",
            "original-price-descending": "-original_price",
            "original-price-ascending" : "original_price"
        }
        q = Q()
        if author_id:
            q &= Q(author_id__in = author_id)
        if theme_id:
            q &= Q(theme__in = theme_id)
        if color_id:
            q &= Q(color__in = color_id)
        if size_id:
            q &= Q(size__in = size_id)
            
        products = Product.objects.filter(q).order_by(options.get(sort, None))
        count    = products.count()
    
        productslist = [
            {
            "author_id"     : product.author.id,
            "product_id"    : product.id,
            "product_name"  : product.name,
            "product_price" : product.current_buying_price if sort == "buying-price-ascending" else\
                                (product.current_selling_price if sort == "selling-price-descending" else product.original_price),
            "sort_name"     : "즉시 구매가순" if sort == "buying-price-ascending" else\
                                ("즉시 판매가순" if sort == "selling-price-descending" else "발매가순"),
            "author_name"   : product.author.name,
            "image"         : [image.image_url for image in product.productimage_set.all()],
            } for product in products[offset:limit]
        ]
        return JsonResponse({"product_count":count, "results":productslist}, status = 200)

class ProductDetailView(View):
    @query_debugger
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'message':'INVALID_ERROR'}, status=404)     

        product = Product.objects.prefetch_related(
            'productcolor_set__color',
            'bidding_set', 
            'productimage_set',
            Prefetch('bidding_set', queryset=Bidding.objects.filter(status_id=1, is_seller=1).order_by('-price', 'created_at'), to_attr="selling_bidding"),
            Prefetch('bidding_set', queryset=Bidding.objects.filter(status_id=1, is_seller=0).order_by('-price', 'created_at'), to_attr="buying_bidding"),
        ).get(id=product_id)
        
        contract_choice = request.GET.get('contract_choice', '1w')
        contract_period = {
            '3m':datetime.now()-relativedelta(months=3),
            '1m':datetime.now()-relativedelta(months=1),
            '1w':datetime.now()-timedelta(weeks=1)
        }
        contract_all = Contract.objects.select_related('selling_bid__product').filter(selling_bid__product=product_id)
        contracts    = contract_all.filter(created_at__range=(contract_period[contract_choice], datetime.now())).order_by('-created_at')

        if contracts.count() >= 2:
            latest_price          = contracts[0].selling_bid.price
            old_price             = contracts[1].selling_bid.price
            comparing_price       = latest_price - old_price
            comparing_price_ratio = round((comparing_price / old_price) * 100, 1)
        else:
            latest_price = comparing_price = comparing_price_ratio = 0

        main_info = {
            'name'                     : product.name,
            'recent_price'             : contracts[0].selling_bid.price if contracts[0].selling_bid.price else 0,
            'oldest_selling_bidding_id': product.selling_bidding[0].id if product.selling_bidding else None,
            'oldest_buying_bidding_id' : product.buying_bidding[0].id if product.buying_bidding else None,
            'current_selling_price'    : product.selling_bidding[0].price if product.selling_bidding else None,
            'current_buying_price'     : product.buying_bidding[0].price if product.buying_bidding else None,
            'image_url'                : [image.image_url for image in product.productimage_set.all()],
            'comparing_price'          : comparing_price,
            'comparing_price_ratio'    : comparing_price_ratio
        }

        contract_all = [{
            'contract_date' :contract.created_at.strftime('%Y-%m-%d'), 
            'contract_price':contract.selling_bid.price
        } for contract in contract_all]

        contract_detail = [{
            'contract_date' :contract.created_at.strftime('%Y-%m-%d'),
            'contract_price':contract.selling_bid.price
        } for contract in contracts]

        bidding_detail  = {
            'selling_bidding':[{
                'selling_bidding_date' : selling_bidding.created_at.strftime('%Y-%m-%d'),
                'selling_bidding_price' :selling_bidding.price
            } for selling_bidding in product.selling_bidding],
            'buying_bidding':[{
                'buying_bidding_date':buying_bidding.created_at.strftime('%Y-%m-%d'),
                'buying_bidding_price':buying_bidding.price
            } for buying_bidding in product.buying_bidding],
        }

        product_info = {
            'model_number'  :product_id,
            'author'        :product.author.name,
            'color'         :[product_color.color.name for product_color in product.productcolor_set.all()],
            'original_price':product.original_price
        }

        return JsonResponse({
            'message'        :'SUCCESS',
            'main_info'      :main_info,
            'contract_detail':contract_detail,
            'contract_all'   :contract_all,
            'bidding_detail' :bidding_detail,
            'product_info'   :product_info},
        status=200)