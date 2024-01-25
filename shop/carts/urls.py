from django.urls import path

from .views import CartProductListView, AddToCartView

urlpatterns = [
    path(r'cart/', CartProductListView.as_view(), name='cart'),
    path(r'add_cart/<int:pk>', AddToCartView.as_view(), name='add_to_cart'),
]
