from django.db import models

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Bidding(TimeStampModel):
    expired_within = models.ForeignKey('ExpiredWithin', on_delete=models.SET_NULL, null=True)
    is_seller      = models.BooleanField()
    user           = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    product        = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    price          = models.DecimalField(max_digits=18, decimal_places=2)
    status         = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True) 

    class Meta:
        db_table = 'biddings'

class Contract(TimeStampModel):
    selling_bid = models.OneToOneField('Bidding', unique=True, related_name='selling_bid', on_delete=models.SET_NULL, null=True)
    buying_bid  = models.OneToOneField('Bidding', unique=True, related_name='buying_bid', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'contracts'

class Status(models.Model):
    ON_BIDDING = 1
    EXPIRED    = 2
    CONTRACTED = 3

    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'statuses'

class ExpiredWithin(models.Model):
    period = models.IntegerField()

    class Meta:
        db_table = 'expired_within'