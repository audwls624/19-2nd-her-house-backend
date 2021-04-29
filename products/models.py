from django.db import models

class Category(models.Model):
    name      = models.CharField(max_length=20)
    image_url = models.URLField(max_length=2000)
    
    class Meta:
        db_table = 'categories'

class Product(models.Model):
    category           = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    name               = models.CharField(max_length=45)
    price              = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rate      = models.DecimalField(max_digits=3, decimal_places=2)
    is_freedelivery    = models.BooleanField(default=False)
    delivery_fee       = models.DecimalField(max_digits=5, decimal_places=2)
    delivery_method    = models.BooleanField(default=False)
    thumbnail_image    = models.URLField(max_length=2000)
    manufacturer       = models.CharField(max_length=45)
    description        = models.CharField(max_length=100)
    description_image  = models.URLField(max_length=2000)
    color              = models.ManyToManyField('Color', through='ProductOption')
    size               = models.ManyToManyField('Size', through='ProductOption')
    user               = models.ManyToManyField('users.User',through='Review',related_name='user_review')

    class Meta:
        db_table = 'products'

class Color(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'

class Size(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'sizes'


class ProductOption(models.Model):
    size    = models.ForeignKey('Size', on_delete=models.CASCADE)
    color   = models.ForeignKey('Color', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_options'

class ProductImage(models.Model):
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'product_images'

class Review(models.Model):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product     = models.ForeignKey('Product', on_delete=models.CASCADE)
    star_rating = models.DecimalField(max_digits=3, decimal_places=2)
    image_url   = models.URLField(max_length=2000)
    text        = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'reviews'