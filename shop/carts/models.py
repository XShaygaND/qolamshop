from django.db import models

from users.models import User
from products.models import Product


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Cart | ' + str(self.owner) + ' | ' + str(self.count)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return ' | '.join((str(self.cart.owner), str(self.product.name), str(self.quantity)))