from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from carts.models import Cart


@receiver(post_save, sender=User)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    """A signal that creates a Cart model for each user upon creation"""
    
    if created:
        Cart.objects.create(owner=instance)
