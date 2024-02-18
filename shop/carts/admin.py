from django.contrib import admin

from carts.models import Cart, CartItem, Order


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'count',
        'is_active'
        )
    
    list_filter = ('is_active',)
    search_fields = ('owner__email',)
    readonly_fields = ('count', 'is_active')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cart',
        'product',
        'quantity'
        )
    
    list_filter = ('cart__is_active',)
    search_fields = ('cart__owner__email',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cart',
        'delivery_method',
        'status'
        )
    
    list_filter = ('delivery_method', 'status')
    search_fields = ('cart__owner__email',)
