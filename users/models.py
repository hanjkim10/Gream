from django.db import models

class User(models.Model):
    email        = models.EmailField(unique=True)
    password     = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=45, unique=True)
    kakao_id     = models.CharField(max_length=45, null=True)
    card_company = models.CharField(max_length=45, null=True)
    card_numnber = models.CharField(max_length=45, null=True)
    address      = models.CharField(max_length=128, null=True)

    class Meta:
        db_table = 'users'