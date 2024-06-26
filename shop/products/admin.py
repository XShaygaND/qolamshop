from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'owner',
        'price',
        'count',
        'category'
        )

    list_filter = ('owner', 'category')
    search_fields = ('name',)

    def get_exclude(self, request, obj = ...):
        return ('sales',)
