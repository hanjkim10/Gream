from drf_yasg import openapi

products_schema_dict = {
    "201": openapi.Response(
        description="성공",
        examples={
            "application/json": {
                'message': 'SUCCESS',
                "count": 103}})}