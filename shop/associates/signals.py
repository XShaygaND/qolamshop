from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from associates.models import Associate


@receiver(post_save, sender=Associate)
def update_user_card_count(sender, instance, created, **kwargs):
    """Signal which handles token creation for the associate"""

    if created:
        Token.objects.create(user=instance.owner)
        return

    elif not instance.is_active:
        try:
            token = Token.objects.get(user=instance.owner)

        except Token.DoesNotExist:
            token = None

        if token:
            token.delete()
    
    else:
        try:
            token = Token.objects.get(user=instance.owner)

        except Token.DoesNotExist:
            token = None

        if not token:
            Token.objects.create(user=instance.owner)


@receiver(post_delete, sender=Associate)
def update_user_card_count(sender, instance, created, **kwargs):
    """Signal which handles token deletion for the associate"""

    try:
        token = Token.objects.get(user=instance.owner)

    except Token.DoesNotExist:
        token = None

    if token:
        token.delete()
