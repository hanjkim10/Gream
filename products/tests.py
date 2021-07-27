import json
import unittest

from django.test      import TestCase, Client
from django.db.models import Q
from .models          import *

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
                "product_id"                : 1,
                "product_name"              : "Topsy Emerie Quinten Maddison Poster",
                "product_buying_price"      : "8299000.00",
                "product_buying_price_name" : "즉시 구매가순",
                'product_selling_price'     : "2125000.00",
                "product_selling_price_name": "즉시 판매가순",
                "product_original_price"    : "654000.00",
                "author_name"               : "Bianka Anastazija",
                "image"                     : ["https://images.unsplash.com/photo-1597873618537-64a04f9e1fb3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8Mnx8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080"]
            },
            {
                "product_id"                : 2,
                "product_name"              : "Lynnette Kimberlyn Jonah Webster poster",
                "product_buying_price"      : "8574000.00",
                "product_buying_price_name" : "즉시 구매가순",
                'product_selling_price'     : "1950000.00",
                "product_selling_price_name": "즉시 판매가순",
                "product_original_price"    : "20000.00",
                "author_name"               : "Shantelle Bruno",
                "image"                     : ["https://images.unsplash.com/photo-1600164318544-79e55da1ac8f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8M3x8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080"]
            },
            {
                "product_id"                : 3,
                "product_name"              : "Benson Adrianne Joshua Katey poster",
                "product_buying_price"      : "9023000.00",
                "product_buying_price_name" : "즉시 구매가순",
                'product_selling_price'     : "1164000.00",
                "product_selling_price_name": "즉시 판매가순",
                "product_original_price"    : "19000.00",
                "author_name"               : "Amour Grenville",
                "image"                     : ["https://images.unsplash.com/photo-1580981454083-eca7032db2c3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMjA3fDB8MXxzZWFyY2h8NHx8cG9zdGVyfHwwfDJ8fHwxNjI2Njg4OTQ0&ixlib=rb-1.2.1&q=80&w=1080"]
            }
        ]

        response = client.get('/products')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"results":productlist})
        
