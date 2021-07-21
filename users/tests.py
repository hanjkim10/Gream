import json
import bcrypt

from django.test  import TestCase, Client

from users.models import User

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
            'email'       :'leecode@gmail.com',
            'password'    :'1234@yyyy',
            'name'        :'이코드'
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

