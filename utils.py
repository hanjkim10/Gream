import jwt

from django.http import JsonResponse

from gream.settings import SECRET_KEY, ALGORITHMS
from users.models   import User

def authorization(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)

        if not access_token:
            return JsonResponse({'error': 'ACESS_TOKEN_REQUIRED'}, status=401)

        try:
            payload = jwt.decode(access_token, SECRET_KEY, ALGORITHMS)

            if not User.objects.filter(id=payload['user_id']).exists():
                return JsonResponse({'message': 'INVALID_USER'}, satus=400)

            request.user = User.objects.get(id=payload['user_id'])
            return func(self, request, *args, **kwargs)
            

        except jwt.InvalidSignatureError:
            return JsonResponse({'error':'INVALID_TOKEN'}, status=400)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error':'EXPIRED_SIGNATURE'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'error':'INVALID_TOKEN'}, status=401)
            
    return wrapper