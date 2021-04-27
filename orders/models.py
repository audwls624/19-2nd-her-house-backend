from django.db import models

class Cart(models.Model):
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product    = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    order      = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity   = models.IntegerField()

    class Meta:
        db_table = 'carts'

class OrderStatus(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'order_statuses'

class Order(models.Model):
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True, null=True)
    total_price    = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = models.IntegerField()
    order_status   = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'
