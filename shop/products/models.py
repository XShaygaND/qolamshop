from django.db import models
from django.urls import reverse

from products.datasets import categories, holdings
from associates.models import Associate


class Product(models.Model):
    name = models.CharField(max_length=99)
    description = models.TextField(max_length=1999)
    logo = models.ImageField(blank=False)
    price = models.FloatField()
    sales = models.PositiveIntegerField(default=0)
    count = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=99, choices=categories)
    owner = models.ForeignKey(Associate, on_delete=models.CASCADE)
    holding = models.CharField(max_length=99, choices=holdings)

    def get_absolute_url(self):
        return reverse("products:details", kwargs={"pk": self.pk})
    
    def __str__(self):
        return ' | '.join((str(self.owner), self.name, '$' + str(self.price)))
