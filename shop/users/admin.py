from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'is_associate',
        'is_active',
        'is_staff',
        'is_superuser'
    )

    list_filter = (
        'is_associate',
        'is_active',
        'is_staff',
        'is_superuser'
    )

    search_fields = (
        'email',
    )

    readonly_fields = ('email', 'purchases', 'cart_count')

    fieldsets = [
        (
            None,
            {
                'fields': ['email', 'purchases', 'cart_count', 'date_joined'],
            },
        ),
        (
            'stats',
            {
                "classes": ["collapse"],
                'fields': ['is_superuser', 'is_staff', 'is_active', 'is_associate', 'last_login']
            }
        )
    ]
