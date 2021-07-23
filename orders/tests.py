import jwt, json

from django.test     import TestCase, Client

from users.models    import User
from products.models import Product, Author, ProductImage, Size
from orders.models   import Bidding, Contract, ExpiredWithin, Status
from gream_settings  import SECRET_KEY, ALGORITHMS

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