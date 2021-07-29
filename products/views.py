import json
from django.db.models.aggregates import Max

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q, Count

from products.models    import Author, Theme, Color, Size, Product

class BestAuthorView(View):
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
    def get(self, request):
        author_id = request.GET.getlist("author", None)
        theme_id  = request.GET.getlist("theme", None)
        color_id  = request.GET.getlist("color", None)
        size_id   = request.GET.getlist("size", None)
        sort      = request.GET.get("sort", "buying-price-ascending")
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