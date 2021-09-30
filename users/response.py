from drf_yasg import openapi

users_schema_dict = {
    "201": openapi.Response(
        description="성공",
        examples={
            "application/json": {
                'message': 'SUCCESS',
                "count": 103}})}