from django.db.models.signals import post_save
from django.dispatch import receiver

from carts.models import CartItem  


@receiver(post_save, sender=CartItem)
def update_user_card_count(sender, instance, created, **kwargs):
    """A signal that updates the `carts.models.Cart.count` and `users.models.User.cart_count` post_save"""
    
    if created:
        cart = instance.cart
        user = instance.cart.owner

        cart.count += instance.quantity
        user.cart_count += instance.quantity

        cart.save()
        user.save()
