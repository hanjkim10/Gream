from orders.models import Status
import re, json, bcrypt, jwt, requests
from datetime         import datetime, timedelta

from django.views     import View
from django.http      import JsonResponse
from django.shortcuts import redirect

from users.models    import User
from gream.settings  import SECRET_KEY, ALGORITHMS
from utils           import authorization

from users.response  import users_schema_dict

from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

REGEX = {
    'email'    : '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    'password' : '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%#?&])[A-Za-z\d@$!%*#?&]{8,16}$'
}

class SignupView(APIView):
    @swagger_auto_schema(manual_parameters = [], responses = users_schema_dict)
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
            name         = data['name']

            if not re.match(REGEX['email'], email) or not re.match(REGEX['password'], password):
                return JsonResponse({'message':'INVALID_ERROR'}, status=400)
            
            if User.objects.filter(email=email).exists() or User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'message':'DUPLICATE'},status=409)
            
            encoded_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                email        = email,
                password     = encoded_password.decode('utf-8'),
                phone_number = phone_number,
                name         = name
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'INVALID_USER'},status=401)
            
            email    = data['email']
            password = data['password']
            user_id  = User.objects.get(email=email).id

            if bcrypt.checkpw(password.encode('utf-8'), User.objects.get(id=user_id).password.encode('utf-8')):
                access_token = jwt.encode({'user_id':user_id, 'exp':datetime.utcnow()+timedelta(days=1)},SECRET_KEY,algorithm=ALGORITHMS)
                return JsonResponse({'message':'SUCCESS', 'TOKEN':access_token}, status=200)

            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class UserView(View):
    @authorization
    def get(self, request):
        user = request.user

        results = {
            'name': user.name,
            'address': user.address,
            'phone_number': user.phone_number,
            'payment': {
                'card_company': user.card_company,
                'card_number': user.card_number,
                'bank_name': user.bank_name,
                'bank_account':user.bank_account
            }
        }

        return JsonResponse({'results': results}, status=200)

class KakaoSigninView(View):
    def get(self, request):
        access_token     = request.headers.get('Authorization')
        profile_request  = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"}).json()
        user, is_created = User.objects.get_or_create(kakao_id = profile_request["id"])
        access_token     = jwt.encode({'user_id':user.id, 'exp':datetime.utcnow()+timedelta(days=1)},SECRET_KEY,algorithm=ALGORITHMS)

        if is_created:
            user.email = profile_request['kakao_account']["email"]
            user.save()
            return JsonResponse({'message':'SUCCESS', 'TOKEN':access_token}, status=201)
        return JsonResponse({'message':'SUCCESS', 'TOKEN':access_token}, status=200)