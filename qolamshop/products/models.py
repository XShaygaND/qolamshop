from django.db import models

class Seller(models.Model):
    name = models.CharField(max_length=255, required=True, blank=False)
    description = models.TextField(max_length=1275, required=False)
    join_date = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=-1)
    logo = models.ImageField(required=True)
    sale_count = models.IntegerField(default=0)


class Product(models.Model):
    """
    A model for each product in the shop
    """

    name = models.CharField(max_length=255, required=True, blank=False)
    description = models.TextField(max_length=1275, required=False)
    price = models.FloatField(required=True, blank=False)
    rate = models.IntegerField(default=-1)
    delivery_delay = models.IntegerField(default=0)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(required=True)
    sale_count = models.IntegerField(default=0)


class ProductImages(models.Model):
    """
    A model created for the Product model for it to be able to include multiple images
    """

    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(required=False)
