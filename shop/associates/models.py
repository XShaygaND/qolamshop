from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from associates.datasets import locations


User = get_user_model()

class Associate(models.Model):
    """A simple model representing the associates of the shop"""

    name = models.CharField(max_length=99)
    description = models.TextField(max_length=1999)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(blank=False)
    join_date = models.DateTimeField(auto_now_add=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=99, choices=locations, blank=False)
    slug = models.SlugField(blank=False)

    def get_absolute_url(self):
        return reverse('associate', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name
