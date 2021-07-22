import json, bcrypt, jwt
from datetime       import datetime, timedelta

from django.test    import TestCase, Client

from users.models   import User
from gream.settings import SECRET_KEY, ALGORITHMS

class SignupTest(TestCase):
    def setUp(self):
        User.objects.create(
            id           = 1,
            email        = 'kimcode@gmail.com',
            password     = '1234@yyyy',
            phone_number = '01090908080',
            name         = '김코드'
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signupview_post_success(self):
        client = Client()
        user= {
            'email'       :'leecode@gmail.com',
            'password'    :'1234@yyyy',
            'phone_number':'01090901111',
            'name'        :'이코드'
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), 
            {
                'message' : 'SUCCESS'
            }
        )

    def test_signupview_post_invalid_email(self):
        client = Client()
        user= {
            'email'       :'leecode',
            'password'    :'1234@yyyy',
            'phone_number':'01090901111',
            'name'        :'이코드'
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'error':'INVALID_ERROR'
            }
        )

    def test_signupview_post_invalid_password(self):
        client = Client()
        user= {
            'email'       :'leecode',
            'password'    :'1234',
            'phone_number':'01090901111',
            'name'        :'이코드'
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'error':'INVALID_ERROR'
            }
        )

    def test_signupview_post_duplicated_email(self):
        client = Client()
        user= {
            'email'       :'kimcode@gmail.com',
            'password'    :'1234@yyyy',
            'phone_number':'01090901111',
            'name'        :'이코드'
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), 
            {
                'message':'DUPLICATE'
            }
        )

    def test_signupview_post_duplicated_phone_number(self):
        client = Client()
        user= {
            'email'       :'leecode@gmail.com',
            'password'    :'1234@yyyy',
            'phone_number':'01090908080',
            'name'        :'이코드'
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), 
            {
                'message':'DUPLICATE'
            }
        )

    def test_signupview_post_keyerror_email(self):
        client = Client()
        user= {
            'password'    :'1234@yyyy',
            'phone_number':'01090901111',
            'name'        :'이코드'
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message':'KEY_ERROR'
            }
        )

    def test_signupview_post_keyerror_password(self):
        client = Client()
        user= {
            'email'       :'leecode@gmail.com',
            'phone_number':'01090901111',
            'name'        :'이코드'
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message':'KEY_ERROR'
            }
        )

    def test_signupview_post_keyerror_phone_number(self):
        client = Client()
        user= {
            'email'   :'leecode@gmail.com',
            'password':'1234@yyyy',
            'name'    :'이코드'
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message':'KEY_ERROR'
            }
        )

    def test_signupview_post_keyerror_name(self):
        client = Client()
        user= {
            'email'       :'leecode@gmail.com',
            'password'    :'1234@yyyy',
            'phone_number':'01090901111',
        }
        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message':'KEY_ERROR'
            }
        )

class SigninTest(TestCase):
    def setUp(self):
        password='1234@yyyy'
        User.objects.create(
            id           = 1,
            email        = 'kimcode@gmail.com',
            password     = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            phone_number = '01090908080',
            name         = '김코드'
        )

    def test_signinview_post_success(self):
        client = Client()
        user= {
            'email'   :'kimcode@gmail.com',
            'password':'1234@yyyy'
        }
        response     = client.post('/users/signin', json.dumps(user), content_type='application/json')
        access_token = response.json()['TOKEN']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'message': 'SUCCESS',
                'TOKEN'  : access_token
            }
        )

    def test_signinview_post_user_does_not_exists(self):
        client = Client()
        user= {
            'email'   :'leecode@gmail.com',
            'password':'1234@yyyy'
        }
        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                'message':'INVALID_USER'
            }
        )

    def test_signinview_post_password_does_not_match(self):
        client = Client()
        user= {
            'email'   :'kimcode@gmail.com',
            'password':'1234@tttt'
        }
        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 
            {
                'message':'INVALID_USER'
            }
        )

    def test_signinview_post_keyerror_email(self):
        client = Client()
        user= {
            'password':'1234@yyyy'
        }
        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message':'KEY_ERROR'
            }
        )

    def test_signinview_post_keyerror_password(self):
        client = Client()
        user= {
            'email':'kimcode@gmail.com',
        }
        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message':'KEY_ERROR'
            }
        )

    def tearDown(self):
        User.objects.all().delete()