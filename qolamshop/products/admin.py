from django.contrib import admin
from .models import Product, ProductImage, Seller


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


class SellerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'join_date',
                'name',
                'description',
            ),

        }),
        ('Advanced information', {

            'fields': (
                'sale_count',
                'rate',
                'logo',
            )
        })
    )
    list_display = ('name', 'join_date', 'sale_count', 'rate')
    list_filter = ('join_date', 'rate')
    search_fields = ('name',)
    readonly_fields = ('join_date', 'rate', 'sale_count')


class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'pub_date',
                'name',
                'description',
                'price',
            ),
        }),
        ('Advanced information', {
            'fields': (
                'sale_count',
                'rate',
                'seller',
                'delivery_delay',
                'main_image',
            )
        })
    )
    list_display = ('name', 'seller', 'price', 'sale_count', 'delivery_delay')
    list_filter = ('pub_date',)
    search_fields = ('name', 'seller__name')
    inlines = (ProductImageInline,)
    readonly_fields = ('pub_date', 'rate', 'sale_count')


admin.site.register(Seller, SellerAdmin)
admin.site.register(Product, ProductAdmin)
