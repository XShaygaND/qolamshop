from django.contrib import admin

from carts.models import Cart, CartItem


admin.site.register((Cart, CartItem))
