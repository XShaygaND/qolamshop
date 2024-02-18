from django.db import models

from users.models import User
from products.models import Product
from carts.datasets import delivery_methods, order_statuses


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return ' | '.join((str(self.owner), str(self.count), str(self.is_active)))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return ' | '.join((str(self.cart.owner), str(self.product.name), str(self.quantity)))
    

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.TextField(max_length=199, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    delivery_method = models.CharField(max_length=99, choices=delivery_methods, default="ND")
    status = models.CharField(max_length=99, choices=order_statuses, default='CRT')

    def __str__(self):
        return ' | '.join(('Order', str(self.cart.owner), str(self.cart.count), str(self.status)))
