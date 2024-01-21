from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path(r'', include(('products.urls', 'products'))),
    path(r'', include(('associates.urls', 'associates'))),
    path(r'', include(('users.urls', 'users'))),
    path(r'admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
