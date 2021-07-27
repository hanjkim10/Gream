import json, jwt
import unittest

from django.test      import TestCase, Client
from django.db.models import Q
from django.utils     import timezone
from datetime         import datetime

from products.models  import Product, Author, ProductImage, Size, Color, Theme, ProductTheme, ProductColor
from orders.models    import ExpiredWithin, Bidding, Contract, Status
from users.models     import User
from gream.settings   import SECRET_KEY, ALGORITHMS

class CategoryTest(TestCase):
    def setUp(self):
        Author.objects.create(
            name = "Bianka Anastazija",
            id   = 1
        )
        Theme.objects.create(
            name = "팝아트",
            id   = 2
        )
        Color.objects.create(
            name = "Red",
            id   = 1
        )
        Size.objects.create(
            name = "3",
            id   = 3,
        )
    def tearDown(self):
        Author.objects.all().delete()
        Theme.objects.all().delete()
        Color.objects.all().delete()
        Size.objects.all().delete()
    def test_categoryview_get_success(self):
        client  = Client()
        results = [
            {
                "category_name": "작가",
                "option"       : [
                    {
                        "name": "Bianka Anastazija",
                        "id"  : 1
                    } 
                ]},
            {
                "category_name": "테마",
                "option"       : [
                    {
                        "name": "팝아트",
                        "id"  : 2
                    }
                ]},
            {
                "category_name": "색상",
                "option"       : [
                    {
                        "name": "Red",
                        "id"  : 1
                    }
                ]},
            {
                "category_name": "크기",
                "option"       : [
                    {
                        "name": "3",
                        "id"  : 3
                    } 
                ]}
        ]
        response = client.get('/products/category')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"results":results})
class ProductTest(TestCase):
    def setUpTestData():
        Author.objects.create(
            name = "Bianka Anastazija",
            id   = 1
        )
        Author.objects.create(
            name = "Shantelle Bruno",
            id   = 2
        )
        Author.objects.create(
            name = "Amour Grenville",
            id   = 3
        )
        Theme.objects.create(
            name = "팝아트",
            id   = 2
        )
        Theme.objects.create(
            name = "만화",
            id   = 6
        )
        Theme.objects.create(
            name = "서양화",
            id   = 3
        )
        Color.objects.create(
            id         = 1,
            name = "Red",
            hex        = "#FF0000",
            rgb        = "255,0,0"
        )
        Color.objects.create(
            id         = 2,
            name = "Green",
            hex        = "#008000",
            rgb        = "0,128,0"
        )
        Color.objects.create(
            id         = 3,
            name = "Blue",
            hex        = "#0000FF",
            rgb        = "0,0,255"
        )
        Size.objects.create(
            name = "3",
            id   = 3
        )
        Size.objects.create(
            name = "4",
            id   = 4
        )
        Size.objects.create(
            name = "1",
            id   = 1
        )
        Product.objects.create(
            id                    = 1,
            name                  = "Topsy Emerie Quinten Maddison Poster",
            current_buying_price  = 8299000,
            current_selling_price = 2125000,
            original_price        = 654000,
            author_id             = 1,
            size_id               = 3
        )
        Product.objects.create(
            id                    = 2,
            name                  = "Lynnette Kimberlyn Jonah Webster poster",
            current_buying_price  = 8574000,
            current_selling_price = 1950000,
            original_price        = 20000,
            author_id             = 2,
            size_id               = 4
        )
        Product.objects.create(
            id                    = 3,
            name                  = "Benson Adrianne Joshua Katey poster",
            current_buying_price  = 9023000,
            current_selling_price = 1164000,
            original_price        = 19000,
            author_id             = 3,
            size_id               = 1
        )
        ProductImage.objects.create(
            id         = 1,
            product_id = 1,
            image_url  = "https://images.unsplash.com/photo-1597873618537-64a04f9e1fb3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8Mnx8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080"   
        )
        ProductImage.objects.create(
            id         = 2,
            product_id = 2,
            image_url  = "https://images.unsplash.com/photo-1600164318544-79e55da1ac8f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8M3x8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080"
        )
        ProductImage.objects.create(
            id         = 3,
            product_id = 3,
            image_url  = "https://images.unsplash.com/photo-1580981454083-eca7032db2c3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8NHx8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080"
        )
        ProductColor.objects.create(
            id         = 1,
            product_id = 1,
            color_id   = 1
        )
        ProductColor.objects.create(
            id         = 2,
            product_id = 2,
            color_id   = 2
        )
        ProductColor.objects.create(
            id         = 3,
            product_id = 3,
            color_id   = 3
        )
        ProductTheme.objects.create(
            id         = 1,
            theme_id   = 2,
            product_id = 1
        )
        ProductTheme.objects.create(
            id         = 2,
            theme_id   = 6,
            product_id = 2
        )
        ProductTheme.objects.create(
            id         = 3,
            theme_id   = 3,
            product_id = 3
        )
    def tearDown(self):
        Author.objects.all().delete()
        Theme.objects.all().delete()
        Color.objects.all().delete()
        Size.objects.all().delete()
    def test_productview_get_success(self):
        client  = Client()
        productlist = [
            {
                "author_id"                 : 1,
                "product_id"                : 1,
                "product_name"              : "Topsy Emerie Quinten Maddison Poster",
                "product_price"             : "2125000.00",
                "sort_name"                 : "즉시 판매가순",
                "author_name"               : "Bianka Anastazija",
                "image"                     : ["https://images.unsplash.com/photo-1597873618537-64a04f9e1fb3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8Mnx8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080"]
            },
            {
                "author_id"                 : 2,
                "product_id"                : 2,
                "product_name"              : "Lynnette Kimberlyn Jonah Webster poster",
                "product_price"             : "1950000.00",
                "sort_name"                 : "즉시 판매가순",
                "author_name"               : "Shantelle Bruno",
                "image"                     : ["https://images.unsplash.com/photo-1600164318544-79e55da1ac8f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8M3x8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080"]
            },
            {
                "author_id"                 : 3,
                "product_id"                : 3,
                "product_name"              : "Benson Adrianne Joshua Katey poster",
                "product_price"             : "1164000.00",
                "sort_name"                 : "즉시 판매가순",
                "author_name"               : "Amour Grenville",
                "image"                     : ["https://images.unsplash.com/photo-1580981454083-eca7032db2c3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8NHx8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080"]
            }
        ]
        response = client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"results":productlist})

class ProductDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(
            id   = 1, 
            name = "김작가"
        )

        size = Size.objects.create(
            id   = 1, 
            name ='1호'
        )

        product = Product.objects.create(
            id                    = 1,
            name                  = "멋진그림",
            current_buying_price  = 2000.00,
            current_selling_price = 2000.00,
            author                = author,
            size                  = size,
            original_price        = 2000.00
        )

        ProductImage.objects.create(
            id        = 1,
            product   = product, 
            image_url = "test_url1"
        )

        ProductImage.objects.create(
            id        = 2,
            product   = product, 
            image_url = "test_url2"
        )

        ProductImage.objects.create(
            id        = 3,
            product   = product, 
            image_url = "test_url3"
        )

        color = Color.objects.create(
            name = "Red",
            hex  = "#FF0000",
            rgb  = "255,0,0"
        )

        color.product.add(product)

        user_seller = User.objects.create(
            id           = 1,
            email        = 'kimcode@gmail.com',
            password     = '1234@yyyy',
            phone_number = '01090908080',
            name         = '김코드'
        )

        user_buyer = User.objects.create(
            id           = 2,
            email        = 'leecode@gmail.com',
            password     = '1234@yyyy',
            phone_number = '01090907171',
            name         = '이코드'
        )
        
        expired_within = ExpiredWithin.objects.create(
            id     = 1, 
            period = 1
        )

        status_complete = Status.objects.create(
            id   = 1, 
            name = "체결완료"
        )

        status_bidding = Status.objects.create(
            id   = 2, 
            name = "입찰중"
        )

        selling_bidding1 = Bidding.objects.create(
            id             = 1,
            expired_within = expired_within,
            is_seller      = 1,
            user           = user_seller,
            product        = product,
            price          = 2000,
            status         = status_complete
        )

        buying_bidding1 = Bidding.objects.create(
            id             = 2,
            expired_within = expired_within,
            is_seller      = 0,
            user           = user_buyer,
            product        = product,
            price          = 2000,
            status         = status_complete
        )

        selling_bidding2 = Bidding.objects.create(
            id             = 3,
            expired_within = expired_within,
            is_seller      = 1,
            user           = user_seller,
            product        = product,
            price          = 2000,
            status         = status_complete
        )

        buying_bidding2 = Bidding.objects.create(
            id             = 4,
            expired_within = expired_within,
            is_seller      = 0,
            user           = user_buyer,
            product        = product,
            price          = 2000,
            status         = status_complete
        )

        Bidding.objects.create(
            id             = 5,
            expired_within = expired_within,
            is_seller      = 1,
            user           = user_seller,
            product        = product,
            price          = 2000,
            status         = status_bidding
        )

        Bidding.objects.create(
            id             = 6,
            expired_within = expired_within,
            is_seller      = 0,
            user           = user_buyer,
            product        = product,
            price          = 2000,
            status         = status_bidding
        )

        Contract.objects.create(
            id          = 1,
            selling_bid = selling_bidding1,
            buying_bid  = buying_bidding1
        )

        Contract.objects.create(
            id          = 2,
            selling_bid = selling_bidding2,
            buying_bid  = buying_bidding2
        )

    def test_product_detail_get_success(self):
        client   = Client()
        response = client.get('/products/1')
        now      = datetime.today().strftime('%Y-%m-%d')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message": "SUCCESS",
            "main_info": [
                {
                    "name": "멋진그림",
                    "recent_price": "2000.00",
                    "oldest_selling_bidding_id": 1,
                    "oldest_buying_bidding_id": 2,
                    "current_selling_price": "2000.00",
                    "current_buyling_price": "2000.00",
                    "image_url": [
                        "test_url1",
                        "test_url2",
                        "test_url3"
                    ],
                    "comparing_price": "0.00",
                    "comparing_price_ratio": "0.0"
                }
            ],
            "contract_detail": [
                {
                    "contract_date": now,
                    "contract_price": "2000.00"
                },
                {
                    "contract_date": now,
                    "contract_price": "2000.00"
                }
            ],
            "contract_all": [
                {
                    "contract_date": now,
                    "contract_price": "2000.00"
                },
                {
                    "contract_date": now,
                    "contract_price": "2000.00"
                }
            ],
            "bidding_detail": [
                {
                    "selling_bidding": [
                        {
                            "selling_bidding_date": now,
                            "selling_bidding_price": "2000.00"
                        },
                        {
                            "selling_bidding_date": now,
                            "selling_bidding_price": "2000.00"
                        },
                        {
                            "selling_bidding_date": now,
                            "selling_bidding_price": "2000.00"
                        }
                    ],
                    "buying_bidding": [
                        {
                            "buying_bidding_date": now,
                            "buying_bidding_price": "2000.00"
                        },
                        {
                            "buying_bidding_date": now,
                            "buying_bidding_price": "2000.00"
                        },
                        {
                            "buying_bidding_date": now,
                            "buying_bidding_price": "2000.00"
                        }
                    ]
                }
            ],
            "product_info": [
                {
                    "model_number": 1,
                    "author": "김작가",
                    "color": [
                        "Red"
                    ],
                    "original_price": "2000.00"
                }
            ]
        })

    def test_product_detail_get_product_not_found(self):
        client   = Client()
        response = client.get('/products/1000000000')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), 
            {
                'message':'INVALID_ERROR'
            }
        )

    def tearDown(self):
        Author.objects.all().delete()
        Size.objects.all().delete()
        User.objects.all().delete()
        Product.objects.all().delete()
        Bidding.objects.all().delete()
        ExpiredWithin.objects.all().delete()
        Contract.objects.all().delete()
