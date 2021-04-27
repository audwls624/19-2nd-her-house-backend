from django.db import models

class User(models.Model):
    name      = models.CharField(max_length=20)
    nickname  = models.CharField(max_length=20)
    password  = models.CharField(max_length=300)
    email     = models.EmailField(max_length=100)
    order     = models.ManyToManyField('orders.Order',through= 'orders.Cart', related_name='user_order')

    class Meta:
        db_table = 'users'

class Address(models.Model):
    user         = models.ForeignKey('User', on_delete=models.CASCADE)
    user_address = models.CharField(max_length=200)
    is_default   = models.BooleanField(default=False)

    class Meta:
        db_table = 'addresses'