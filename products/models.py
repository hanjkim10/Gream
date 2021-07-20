from django.db import models

class Product(models.Model):
    name                  = models.CharField(max_length=100)
    current_buying_price  = models.DecimalField(max_digits=18, decimal_places=2)
    current_selling_price = models.DecimalField(max_digits=18, decimal_places=2)
    author                = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    size                  = models.ForeignKey('Size', on_delete=models.SET_NULL, null=True)
    original_price        = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'products'

class ProductTheme(models.Model):
    theme   = models.ForeignKey('Theme', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_themes'

class Theme(models.Model):
    name    = models.CharField(max_length=45)
    product = models.ManyToManyField('Product', through='ProductTheme')

    class Meta:
        db_table = 'themes'

class Color(models.Model):
    name    = models.CharField(max_length=45)
    product = models.ManyToManyField('Product', through='ProductColor')
    hex     = models.CharField(max_length=45)
    rgb     = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'

class ProductColor(models.Model):
    color   = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_colors'

class ProductImage(models.Model):
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=256)

    class Meta:
        db_table = 'product_images'

class Author(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'authors'

class Size(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'sizes'