import jwt, functools, time

from django.http    import JsonResponse
from django.db      import connection, reset_queries
from django.conf    import settings

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

def query_debugger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        number_of_start_queries = len(connection.queries)
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        number_of_end_queries = len(connection.queries)
        print(f"-------------------------------------------------------------------")
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {number_of_end_queries-number_of_start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        print(f"-------------------------------------------------------------------")
        return result
    return wrapper