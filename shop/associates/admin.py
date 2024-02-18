from django.contrib import admin

from associates.models import Associate


@admin.register(Associate)
class AssocaiteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'owner',
        'location',
        'sales',
        'is_active'
    )

    list_filter = ('location', 'is_active')
    search_fields = ('owner__email', 'location')
    readonly_fields = ('sales', 'slug')
