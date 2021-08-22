## 프로젝트명: GREAM 🖼
- Kream 클론 프로젝트
- Account, Product category & detail, Order, Bidding 구현
- 초기 세팅부터 모델링과 프론트로 보내주는 모든 제품 data를 실제 사용할 수 있는 서비스 수준으로 개발

<br>

>- 제품 엔드포인트
>   - 베스트 작가 필터링
>```python
>class BestAuthorView(View):
>   def get (self, request):
>       biddings = Count('product__bidding', filter=Q(product__bidding__is_seller=0))
>       popular_biddings = Author.objects.annotate(product_count = biddings).order_by('-product_count')[:4]
>       results = [
>           {
>               "top_author" : topauthor.name,
>               "author_id"  : topauthor.id
>           } for topauthor in popular_biddings
>       ]
>
>       return JsonResponse ({"results":results}, status = 200)
>```
> 
>- 카테고리 필터링
>```python
>class CategoryView(View):
>   def get(self, request):
>       authors  = Author.objects.all()
>       themes   = Theme.objects.all()
>       colors   = Color.objects.all()
>       sizes    = Size.objects.all()
>       results = [
>           {
>               "category_name"   : "author",
>               "category_name_kr": "작가",
>               "option"          : [
>                   {
>                       "name": author.name,
>                       "id"  : author.id
>                   } for author in authors
>               ]},
>           {
>               "category_name"   : "theme",
>               "category_name_kr": "테마",
>               "option"          : [
>                   {
>                       "name": theme.name,
>                       "id"  : theme.id
>                   } for theme in themes
>               ]},
>           {
>               "category_name"   : "color",
>               "category_name_kr": "색상",
>               "option"          : [
>                   {
>                       "name": color.name,
>                       "id"  : color.id
>                   } for color in colors
>               ]},
>           {
>               "category_name"   : "size",
>               "category_name_kr": "크기",
>               "option"          : [
>                   {
>                       "name": size.name,
>                       "id"  : size.id
>                   } for size in sizes
>               ]}
>       ]
>       return JsonResponse ({"results":results}, status = 200)
>```
> 
>- 제품 필터링
>```python
>class ProductView(View):
>   def get(self, request):
>       author_id = request.GET.getlist("author", None)
>       theme_id  = request.GET.getlist("theme", None)
>       color_id  = request.GET.getlist("color", None)
>       size_id   = request.GET.getlist("size", None)
>       sort      = request.GET.get("sort", "original-price-ascending")
>       offset    = int(request.GET.get("offset",0))
>       limit     = int(request.GET.get("limit",100))
>       limit     = offset + limit
>       options   = {
>           "selling-price-descending" : "-current_selling_price",
>           "buying-price-ascending"   : "current_buying_price",
>           "original-price-descending": "-original_price",
>           "original-price-ascending" : "original_price"
>       }
>       q = Q()
>       if author_id:
>           q &= Q(author_id__in = author_id)
>       if theme_id:
>           q &= Q(theme__in = theme_id)
>       if color_id:
>           q &= Q(color__in = color_id)
>       if size_id:
>           q &= Q(size__in = size_id)
>
>       products = Product.objects.filter(q).order_by(options.get(sort, None))
>       count    = products.count()
>       productslist = [
>           {
>           "author_id"     : product.author.id,
>           "product_id"    : product.id,
>           "product_name"  : product.name,
>           "product_price" : product.current_buying_price if sort == "buying-price-ascending" else\
>                               (product.current_selling_price if sort == "selling-price-descending" else product.original_price),
>           "sort_name"     : "즉시 구매가순" if sort == "buying-price-ascending" else\
>                               ("즉시 판매가순" if sort == "selling-price-descending" else "발매가순"),
>           "author_name"   : product.author.name,
>           "image"         : [image.image_url for image in product.productimage_set.all()],
>           } for product in products[offset:limit]
>       ]
>       return JsonResponse({"product_count":count, "results":productslist}, status = 200)
>```

- 주문 엔드포인트
>```python
>class BiddinghistoryView(View):
>    def get(self, request):
>        status_id = request.GET.get("status_id", None)
>        offset    = int(request.GET.get("offset",0))
>        limit     = int(request.GET.get("limit",100))
>        offset    = offset * limit
>        limit     = offset + limit
>        
>        q = Q()
>
>        if status_id:
>            q &= Q(status_id=status_id)
>         
>        biddings = Bidding.objects.select_related('product', 'status').filter(q)[offset:limit]
>
>        biddinglist = [
>            {
>                "product_id"    : bidding.product.id,
>                "product_name"  : bidding.product.name,
>                "is_seller"     : bidding.is_seller,
>                "image"         : bidding.product.productimage_set.first().image_url,
>                "status_id"     : bidding.status.id,
>                "status_name"   : bidding.status.name,
>                "price"         : bidding.price,
>                "bidding_date"  : bidding.updated_at.strftime("%Y.%m.%d"),
>                "expired_date"  : (bidding.updated_at + timezone.timedelta(days=bidding.expired_within.period)).strftime("%Y.%m.%d"),
>            } for bidding in biddings
>        ]
>        return JsonResponse({"results":biddinglist}, status = 200)
>```


### 개발 인원 및 기간

개발기간 : 2021/7/19 ~ 2021/7/30

개발 인원 : 프론트엔드 3명, 백엔드 3명

https://github.com/wecode-bootcamp-korea/22-2nd-GREAM-frontend

https://github.com/wecode-bootcamp-korea/22-2nd-GREAM-backend

### 프론트
박정훈, 오지수, 이경민

### 백엔드
김한준, 서정민, 안재경

### 기술스텍
- python
- django
- MySQL
- RESTful API
- AWS
- PyJWT
- bcrypt

### 구현기능

공통
- 프로젝트 초기 세팅
- Database 모델링 및 ERD

김한준
- 제품 엔드포인트
    - 베스트 작가 필터링
    - 카테고리 필터링
    - 제품 필터링
    - 페이지네이션
- 주문 엔드포인트
    - 구매 내역 필터링
    - 판매 내역 필터링

서정민
- 주문 엔드포인트
    - 판매/구매 입찰 등록 기능 구현
    - 판매/구매 즉시거래 기능 구현
    - 입찰기한에 따른 입찰 상태 업데이트 기능 구현

안재경
- 회원가입 및 로그인(Bcrypt 암호화, JWT 사용, 정규표현식을 사용한 validation)
- 카카오 API를 이용한 소셜로그인 기능 구현
- 사용자 Authentication 확인
- 제품 상세 엔드포인드(상품 정보, 최근 체결거래 가격 기간별 filtering, 해당 상품 체결거래 내역 조회)

Reference
- 이 프로젝트는 Kream 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
