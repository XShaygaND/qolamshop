from django.db import models

class Product(models.Model):
    """
    A model for each product in the shop
    """

    name = models.CharField(max_length=255, required=True, blank=False)
    description = models.TextField(max_length=1275, required=False)
    price = models.FloatField(required=True, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(required=True)


class ProductImages(models.Model):
    """
    A model created for the Product model for it to be able to include multiple images
    """

    product = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(required=False)
