from django.db.models.signals import post_save 
from django.dispatch import receiver

from carts.models import Cart, CartItem, Order


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


@receiver(post_save, sender=Order)
def update_order_cart(sender, instance, created, **kwargs):
    """A signal which updates the cart and the order to prepare it for sending"""

    if created:
        cart = instance.cart
        user = cart.owner
        
        cart.is_active = False
        user.cart_count = 0
        instance.status = 'CFD'

        cart.save()
        user.save()
        instance.save()

        cart = Cart.objects.create(owner=cart.owner)
