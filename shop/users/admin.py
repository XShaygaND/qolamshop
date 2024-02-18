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
