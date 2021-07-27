import jwt, json
import unittest

from django.test     import TestCase, Client

from django.db.models import Q
from users.models     import User
from products.models  import Product, Author, ProductImage, Size, Theme, Size, ProductColor, ProductTheme, Color, ProductColor
from orders.models    import Bidding, Contract, ExpiredWithin, Status
from gream_settings   import SECRET_KEY, ALGORITHMS

class BiddingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            id           = 1,
            email        = 'hi@gmail.com',
            password     = '12345678',
            phone_number = '01012457896',
            kakao_id     = '',
            name         = '서정민',
            card_company = '국민',
            card_number  = '0548-7813-7849-2323',
            bank_name    = '국민',
            bank_account = '451-78469-45',
            address      = '경기도 성남시 야호야호'
        )

        User.objects.create(
            id = 2,
            email        = 'bye@gmail.com',
            password     = '12345678',
            phone_number = '01012457816',
            kakao_id     = '',
            name         = '안재경',
            card_company = '국민',
            card_number  = '0195-7783-7800-0023',
            bank_name    = '국민',
            bank_account = '451-10269-98',
            address      = '서울특별시 야호야호'
        )

        Author.objects.create(
            id   = 1,
            name = '작가님'
        )

        Size.objects.create(
            id   = 1,
            name = 1
        )

        Product.objects.create(
            id                    = 1,
            name                  = 'wow poster',
            current_buying_price  = 0,
            current_selling_price = 0,
            author_id             = 1,
            size_id               = 1,
            original_price        = 20000
        )

        Product.objects.create(
            id                    = 2,
            name                  = 'wooooow poster',
            current_buying_price  = 0,
            current_selling_price = 0,
            author_id             = 1,
            size_id               = 1,
            original_price        = 100000
        )

        Product.objects.create(
            id                    = 3,
            name                  = 'amazing poster',
            current_buying_price  = 0,
            current_selling_price = 0,
            author_id             = 1,
            size_id               = 1,
            original_price        = 50000
        )

        ProductImage.objects.create(
            id         = 1,
            product_id = 1,
            image_url  = 'image_1'
        )

        ProductImage.objects.create(
            id         = 2,
            product_id = 2,
            image_url  = 'image_2'
        )
        
        ProductImage.objects.create(
            id         = 3,
            product_id = 3,
            image_url  = 'image_3'
        )

        Status.objects.create(
            id   = 1,
            name = '입찰중'
        )

        Status.objects.create(
            id   = 3,
            name = '체결 완료'
        )

        ExpiredWithin.objects.create(
            id     = 1,
            period = 1
        )

        global headers
        access_token = jwt.encode({"user_id" : 1}, SECRET_KEY, ALGORITHMS)
        headers      = {'HTTP_AUTHORIZATION': access_token}

    def setUp(self):
        Bidding.objects.create(
            id                = 1,
            is_seller         = 1,
            user_id           = 1,
            product_id        = 1,
            price             = 30000,
            status_id         = 1,
            expired_within_id = 1
        )

        Bidding.objects.create(
            id                = 2,
            is_seller         = 0,
            user_id           = 2,
            product_id        = 2,
            price             = 110000,
            status_id         = 1 ,
            expired_within_id = 1
        )

        Product.objects.filter(id=1).update(current_buying_price=30000)
        Product.objects.filter(id=2).update(current_selling_price=110000)

    def tearDown(self):
        Bidding.objects.all().delete()
        Contract.objects.all().delete()

    def test_bidding_post_view(self):
        client = Client()

        data = {
            "product_id"       : 3,
            "expired_within_id": 1,
            "price"            : 60000
        }

        response = client.post('/orders/bidding?type=buy', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 
            {
                'message': 'NEW_BID_CREATED'
            }
        )

    def test_bidding_post_product_not_found(self):
        client = Client()

        data = {
            "product_id"       : 5,
            "expired_within_id": 1,
            "price"            : 60000
        }

        response = client.post('/orders/bidding?type=buy', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), 
            {
                'message': 'PRODUCT_NOT_FOUND'
            }
        )

    def test_bidding_post_invalid_type(self):
        client = Client()

        data = {
            "product_id"       : 3,
            "expired_within_id": 1,
            "price"            : 60000
        }

        response = client.post('/orders/bidding?type=b', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message': 'INVALID_TYPE'
            }
        )

class ContractTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            id           = 1,
            email        = 'hi@gmail.com',
            password     = '12345678',
            phone_number = '01012457896',
            kakao_id     = '',
            name         = '서정민',
            card_company = '국민',
            card_number  = '0548-7813-7849-2323',
            bank_name    = '국민',
            bank_account = '451-78469-45',
            address      = '경기도 성남시 야호야호'
        )

        User.objects.create(
            id = 2,
            email        = 'bye@gmail.com',
            password     = '12345678',
            phone_number = '01012457816',
            kakao_id     = '',
            name         = '안재경',
            card_company = '국민',
            card_number  = '0195-7783-7800-0023',
            bank_name    = '국민',
            bank_account = '451-10269-98',
            address      = '서울특별시 야호야호'
        )

        Author.objects.create(
            id   = 1,
            name = '작가님'
        )

        Size.objects.create(
            id   = 1,
            name = 1
        )

        Product.objects.create(
            id                    = 1,
            name                  = 'wow poster',
            current_buying_price  = 0,
            current_selling_price = 0,
            author_id             = 1,
            size_id               = 1,
            original_price        = 20000
        )

        Product.objects.create(
            id                    = 2,
            name                  = 'wooooow poster',
            current_buying_price  = 0,
            current_selling_price = 0,
            author_id             = 1,
            size_id               = 1,
            original_price        = 100000
        )

        Product.objects.create(
            id                    = 3,
            name                  = 'amazing poster',
            current_buying_price  = 0,
            current_selling_price = 0,
            author_id             = 1,
            size_id               = 1,
            original_price        = 50000
        )

        ProductImage.objects.create(
            id         = 1,
            product_id = 1,
            image_url  = 'image_1'
        )

        ProductImage.objects.create(
            id         = 2,
            product_id = 2,
            image_url  = 'image_2'
        )
        
        ProductImage.objects.create(
            id         = 3,
            product_id = 3,
            image_url  = 'image_3'
        )

        Status.objects.create(
            id   = 1,
            name = '입찰중'
        )

        Status.objects.create(
            id   = 3,
            name = '체결 완료'
        )

        ExpiredWithin.objects.create(
            id     = 1,
            period = 1
        )

        global headers
        access_token = jwt.encode({"user_id" : 2}, SECRET_KEY, ALGORITHMS)
        headers      = {'HTTP_AUTHORIZATION': access_token}

    def setUp(self):
        Bidding.objects.create(
            id                = 1,
            is_seller         = 1,
            user_id           = 1,
            product_id        = 1,
            price             = 30000,
            status_id         = 1,
            expired_within_id = 1
        )

        Bidding.objects.create(
            id                = 2,
            is_seller         = 0,
            user_id           = 2,
            product_id        = 2,
            price             = 110000,
            status_id         = 1 ,
            expired_within_id = 1
        )

        Product.objects.filter(id=1).update(current_buying_price=30000)
        Product.objects.filter(id=2).update(current_selling_price=110000)

    def tearDown(self):
        Bidding.objects.all().delete()
        Contract.objects.all().delete()

    def test_contract_post_view(self):
        client = Client()

        data = {
            "product_id"    : 1,
            "selling_bid_id": 1,
            "buying_bid_id" : None
        }

        response = client.post('/orders/contract?type=buy', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 
            {
                'message': 'CONTRACT_SUCCESS'
            }
        )

    def test_contract_post_invalid_type(self):
        client = Client()

        data = {
            "product_id"    : 1,
            "selling_bid_id": 1,
            "buying_bid_id" : None
        }

        response = client.post('/orders/contract?type=', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message': 'INVALID_TYPE'
            }
        )

    def test_contract_post_bid_not_found(self):
        client = Client()

        data = {
            "product_id"    : 1,
            "selling_bid_id": None,
            "buying_bid_id" : 5
        }

        response = client.post('/orders/contract?type=sell', json.dumps(data), content_type='application/json', **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), 
            {
                'message': 'BUYING_BID_NOT_FOUND'
            }
        )

class BuyingTest(TestCase):
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
        
        status1 = Status.objects.create(
            id = 3,
            name = "체결 완료"
        )

        user94 = User.objects.create(
            id = 94,
            email = "nwsuf@gmail.com"
        )
        
        user37 = User.objects.create(
            id = 37,
            email = "po@gmail.com"
        )

        user84 = User.objects.create(
            id = 84,
            email = "wqtpu@gmail.com"
        )

        user126 = User.objects.create(
            id = 126,
            email = "vbfbut@naver.com"
        )

        expired60 = ExpiredWithin.objects.create(
            id=5,
            period = 60
        )

        product1 = Product.objects.create(
            id                    = 1,
            name                  = "Topsy Emerie Quinten Maddison Poster",
            current_buying_price  = 8299000,
            current_selling_price = 2125000,
            original_price        = 654000,
            author_id             = 1,
            size_id               = 3
        )

        product2 = Product.objects.create(
            id                    = 2,
            name                  = "Lynnette Kimberlyn Jonah Webster poster",
            current_buying_price  = 8574000,
            current_selling_price = 1950000,
            original_price        = 20000,
            author_id             = 2,
            size_id               = 4
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
        

        Bidding.objects.create(
            id             = 1,
            created_at     = "2021-07-22 07:41:19.755126",
            updated_at     = "2021-07-22 07:41:19.755192",
            is_seller      = 0,
            price          = 7440000.00,
            expired_within = expired60,
            product        = product1,
            status         = status1,
            user        = user94
        )

        Bidding.objects.create(
            id             = 2,
            created_at     = "2021-07-22 07:41:19.755126",
            updated_at     = "2021-07-22 07:41:19.755192",
            is_seller      = 1,
            price          = "7440000.00",
            expired_within = expired60,
            product        = product1,
            status         = status1,
            user        = user37
        )

        Bidding.objects.create(
            id             = 3,
            created_at     = "2021-07-22 07:41:19.761540",
            updated_at     = "2021-07-22 07:41:19.761575",
            is_seller      = 0,
            price          = "8828000.00",
            expired_within = expired60,
            product        = product2,
            status         = status1,
            user        = user84
        )

        Bidding.objects.create(
            id             = 4,
            created_at     = "2021-07-22 07:41:19.762882",
            updated_at     = "2021-07-22 07:41:19.762917",
            is_seller      = 1,
            price          = "8828000.00",
            expired_within = expired60,
            product        = product2,
            status         = status1,
            user       = user126
        )



    def tearDown(self):
        Bidding.objects.all().delete()
        Product.objects.all().delete()
        ProductImage.objects.all().delete()
        Status.objects.all().delete()

    def test_biddinghistory_get_success(self):
        client = Client()
        biddinglist = [
            {
            "product_id": 1,
            "product_name": "Topsy Emerie Quinten Maddison Poster",
            "is_seller": False,
            "image": "https://images.unsplash.com/photo-1597873618537-64a04f9e1fb3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8Mnx8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080",
            "status_id": 3,
            "status_name": "체결 완료",
            "price": "7440000.00",
            "bidding_date": "2021.07.27",
            "expired_date": "2021.09.25"
        },
        {
            "product_id": 1,
            "product_name": "Topsy Emerie Quinten Maddison Poster",
            "is_seller": True,
            "image": "https://images.unsplash.com/photo-1597873618537-64a04f9e1fb3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8Mnx8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080",
            "status_id": 3,
            "status_name": "체결 완료",
            "price": "7440000.00",
            "bidding_date": "2021.07.27",
            "expired_date": "2021.09.25"
        },
        {
            "product_id": 2,
            "product_name": "Lynnette Kimberlyn Jonah Webster poster",
            "is_seller": False,
            "image": "https://images.unsplash.com/photo-1600164318544-79e55da1ac8f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8M3x8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080",
            "status_id": 3,
            "status_name": "체결 완료",
            "price": "8828000.00",
            "bidding_date": "2021.07.27",
            "expired_date": "2021.09.25"
        },
        {
            "product_id": 2,
            "product_name": "Lynnette Kimberlyn Jonah Webster poster",
            "is_seller": True,
            "image": "https://images.unsplash.com/photo-1600164318544-79e55da1ac8f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8M3x8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080",
            "status_id": 3,
            "status_name": "체결 완료",
            "price": "8828000.00",
            "bidding_date": "2021.07.27",
            "expired_date": "2021.09.25"
        }
    ]
 
        response = client.get('/orders/bidding')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"results":biddinglist})