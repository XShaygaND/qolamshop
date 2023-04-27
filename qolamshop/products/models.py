from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


def lower_spacify(text):
    text = str(text)
    return text.replace(' ', '_').lower()


def validate_date_now(date):
    """Raises ValidationError if the join date is any date other than the current time"""
    if date != timezone.now():
        raise ValidationError(
            f'Join date must be set to today\'s date.\n{date}--{timezone.now()}')


def validate_date_past(date):
    """Raises ValidationError if the publish date is any date before the current time"""
    if date < timezone.now():
        raise ValidationError(
            f'publish date must be today or in the future\n{date}--{timezone.now()}')


def get_upload_path(instance, filename):
    """
    Returns appropriate url according to the model.

    `{ls(instance.name)}/logo.png` if the instance is a Seller model
    `{ls(instance.seller.name)}/{ls(instance.name)}/main_image.png` if the instance is a Product Model
    `{ls(instance.product.seller.name)}/{ls(instance.product.name)}/image.png` if the instance is a ProductImage model
    """
    ls = lower_spacify
    if isinstance(instance, Seller):
        return f"{ls(instance.name)}/logo.png"
    elif isinstance(instance, Product):
        return f"{ls(instance.seller.name)}/{ls(instance.name)}/main_image.png"
    return f"{ls(instance.product.seller.name)}/{ls(instance.product.name)}/image.png"


class Seller(models.Model):
    """
    A model for the sellers of the Product model, connected to which with a ForeignKey
    """
    name = models.CharField(max_length=255, blank=False, unique=True)
    description = models.TextField(max_length=1275, blank=False)
    join_date = models.DateTimeField(
        auto_now_add=True, validators=[validate_date_now])
    rate = models.FloatField(default=-1)
    logo = models.ImageField(upload_to=get_upload_path, blank=False)
    sale_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    """
    A model for each product in the shop
    """

    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=1275, blank=True)
    price = models.FloatField(blank=False)
    rate = models.FloatField(default=-1)
    delivery_delay = models.IntegerField(default=0)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        auto_now_add=True, validators=[validate_date_past])
    main_image = models.ImageField(upload_to=get_upload_path, blank=False)
    sale_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ' | by: ' + self.seller.name


class ProductImage(models.Model):
    """
    A model created for the Product model for it to be able to include multiple images
    """

    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path, blank=True)

    def __str__(self):
        return '<ProductImage>' + ' | for: ' + self.product.name
