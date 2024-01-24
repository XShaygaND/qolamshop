from django.db.models.signals import post_save
from django.dispatch import receiver

from carts.models import CartItem  


@receiver(post_save, sender=CartItem)
def update_user_card_count(sender, instance, created, **kwargs):
    """A signal that updates the `carts.models.Cart.count` and `users.models.User.cart_count` fields for the front-end use"""
    
    if created:
        cart = instance.cart
        user = instance.cart.owner

        cart.count += 1
        user.cart_count += 1

        cart.save()
        user.save()
