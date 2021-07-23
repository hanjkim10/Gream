import json

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from products.models    import Author, Theme, Color, Size, Product

class CategoryView(View):
    def get(self, request):
        authors  = Author.objects.all()
        themes   = Theme.objects.all()
        colors   = Color.objects.all()
        sizes    = Size.objects.all()

        results = [
            {
                "category_name": "작가",
                "option"       : [
                    {
                        "name": author.name,
                        "id"  : author.id
                    } for author in authors
                ]},
            {
                "category_name": "테마",
                "option"       : [
                    {
                        "name": theme.name,
                        "id"  : theme.id
                    } for theme in themes
                ]},
            {
                "category_name": "색상",
                "option"       : [
                    {
                        "name": color.name,
                        "id"  : color.id
                    } for color in colors
                ]},
            {
                "category_name": "크기",
                "option"       : [
                    {
                        "name": size.name,
                        "id"  : size.id
                    } for size in sizes
                ]}
            ]
        return JsonResponse ({"results":results}, status = 200)

class ProductView(View):
    def get(self, request):
        author_id = request.GET.get("author", None)
        theme_id  = request.GET.get("theme", None)
        color_id  = request.GET.get("color", None)
        size_id   = request.GET.get("size", None)
        sort      = request.GET.get("sort", "selling-price-descending")
        offset    = int(request.GET.get("offset",0))
        limit     = int(request.GET.get("limit",100))
        offset    = offset * limit
        limit     = offset + limit
        options   = {
            "selling-price-descending" : "-current_selling_price",
            "buying-price-ascending"   : "current_buying_price",
            "original-price-descending": "-original_price",
            "original-price-ascending" : "original_price"
        }

        q = Q()

        if author_id:
            q.add(Q(author_id=author_id), q.AND)
        if theme_id:
            q.add(Q(theme=theme_id), q.AND)
        if color_id:
            q.add(Q(color=color_id), q.AND)
        if size_id:
            q.add(Q(size_id=size_id), q.AND)

        products = Product.objects.filter(q).order_by(options[sort])[offset:limit]

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
            } for product in products
        ]

        return JsonResponse({"results":productslist}, status = 200)