from django.urls import path

from .views import CartProductListView

urlpatterns = [
    path(r'cart/', CartProductListView.as_view(), name='cart'),
]
