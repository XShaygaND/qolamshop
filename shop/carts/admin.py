from django.contrib import admin

from carts.models import Cart, CartItem, Order


admin.site.register((Cart, CartItem, Order))
